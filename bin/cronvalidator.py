import os, sys
from croniter import croniter

cronfield = sys.argv[2] if len(sys.argv) >= 3 else 'cron'

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators


@Configuration()
class StreamingCSC(StreamingCommand):
    """
    The getcronprevsched command returns events with a one new field 'cron_is_valid'.

    Example:

    ``| makeresults count=20 | streamstats count as count| eval cron = "0 0/".count." * * *" | getcronprevsched``

    returns a records with one new field 'cron_is_valid'.
    """

    def stream(self, records):
        # To connect with Splunk, use the instantiated service object which is created using the server-uri and
        # other meta details and can be accessed as shown below
        # Example:-
        #    service = self.service
        #    info = service.info //access the Splunk Server info

        for record in records:
            
            if cronfield in record.keys():
                # Define the cron schedule
                cron_schedule = record[cronfield] 

                # Get the next scheduled time
                record["cron_is_valid"] =  "TRUE" if croniter.is_valid(cron_schedule) else "FALSE"
            yield record


dispatch(StreamingCSC, sys.argv, sys.stdin, sys.stdout, __name__)