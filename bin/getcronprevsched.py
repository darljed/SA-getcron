import os, sys
from croniter import croniter
from datetime import datetime

cronfield = sys.argv[2] if len(sys.argv) >= 3 else 'cron'

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators


@Configuration()
class StreamingCSC(StreamingCommand):
    """
    The getcronprevsched command returns events with a one new field 'cron_prev_schedule'.

    Example:

    ``| makeresults count=5 | streamstats count as count| eval cron = "0 0/".count." * * *" | getcronprevsched``

    returns a records with one new field 'cron_prev_schedule'.
    """

    def stream(self, records):
        # To connect with Splunk, use the instantiated service object which is created using the server-uri and
        # other meta details and can be accessed as shown below
        # Example:-
        #    service = self.service
        #    info = service.info //access the Splunk Server info

        for record in records:
            
            # Define the cron schedule
            if cronfield in record.keys():
                cron_schedule = record[cronfield] 
                if(croniter.is_valid(cron_schedule)):

                    # Get the current time
                    now = datetime.now()

                    # Create a croniter object
                    cron = croniter(cron_schedule, now)

                    # Get the prev scheduled time
                    prev_run = cron.get_prev(datetime)
                    record["cron_prev_schedule"] = prev_run.strftime('%Y-%m-%d %H:%M:%S')
            yield record


dispatch(StreamingCSC, sys.argv, sys.stdin, sys.stdout, __name__)