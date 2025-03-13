import os, sys
from cron_descriptor import Options, CasingTypeEnum, DescriptionTypeEnum, ExpressionDescriptor
from croniter import croniter
from datetime import datetime

cronfield = sys.argv[2] if len(sys.argv) >= 3 else 'cron'
cronfield_prefix = f"{sys.argv[3]}_" if len(sys.argv) >= 4 else ''

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators


@Configuration()
class StreamingCSC(StreamingCommand):
    """
    The getcrondetails command returns events with the following new fields 'cron_is_valid','cron_prev_schedule','cron_next_schedule','cron_description'.

    Example:

    ``| makeresults count=20 | streamstats count as count| eval cron = "0 0/".count." * * *" | getcrondetails``

    returns a records with the following new fields 'cron_is_valid','cron_prev_schedule','cron_next_schedule','cron_description'.
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
                now = datetime.now()
                cron_schedule = record[cronfield] 
                # validator 
                record[f"{cronfield_prefix}cron_is_valid"] =  "TRUE" if croniter.is_valid(cron_schedule) else "FALSE"

                if croniter.is_valid(cron_schedule):
                    cron = croniter(cron_schedule, now)
                    # description
                    options = Options()
                    options.casing_type = CasingTypeEnum.Sentence
                    options.use_24hour_time_format = True
                    descriptor = ExpressionDescriptor(cron_schedule, options)
                    record[f"{cronfield_prefix}cron_description"] = descriptor.get_description()

                    # Get the prev scheduled time
                    prev_run = cron.get_prev(datetime)
                    record[f"{cronfield_prefix}cron_prev_schedule"] = prev_run.strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Get the next scheduled time
                    next_run = cron.get_next(datetime)
                    record[f"{cronfield_prefix}cron_next_schedule"] = next_run.strftime('%Y-%m-%d %H:%M:%S')
            yield record


dispatch(StreamingCSC, sys.argv, sys.stdin, sys.stdout, __name__)