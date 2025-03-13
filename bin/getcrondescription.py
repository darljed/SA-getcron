import os, sys

from croniter import croniter
from cron_descriptor import Options, CasingTypeEnum, DescriptionTypeEnum, ExpressionDescriptor

cronfield = sys.argv[2] if len(sys.argv) >= 3 else 'cron'

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators


@Configuration()
class StreamingCSC(StreamingCommand):
    """
    The getcrondescription command returns events with a one new field 'cron_description' that contains the human readable format of the cron schedule.

    Example:

    ``| makeresults count=5 | streamstats count as count| eval cron = "0 0/".count." * * *" | getcrondescription``

    returns a records with one new fileds 'cron_description'.
    """

    def stream(self, records):

        for record in records:
            if cronfield in record.keys():
                if croniter.is_valid(record[cronfield]): 
                    options = Options()
                    options.casing_type = CasingTypeEnum.Sentence
                    options.use_24hour_time_format = True
                    descriptor = ExpressionDescriptor(record[cronfield], options)
                    record["cron_description"] = descriptor.get_description()
            yield record


dispatch(StreamingCSC, sys.argv, sys.stdin, sys.stdout, __name__)