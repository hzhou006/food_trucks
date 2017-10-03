import datetime


class QueryCurrentFoodTrucks():
    def __init__(self, *args, **kwargs):
        self.datetime_now = datetime.datetime.now()
        self.select_fields = ["applicant", "location"]
        self.num_of_results = 10
        self.offset = kwargs['offset'] * self.num_of_results

    def _format_time(self):
        """
        Returns a string representing the instance's `datetime_now` attribute
        current time in 24 hour format.
        """
        hour24 = "\'{0}:{1}\'".format(
            self.datetime_now.hour,
            str(self.datetime_now.minute).zfill(2)
        )
        return hour24

    def _get_weekday(self):
        """
        Returns instance's `datetime_now` attribute weekday as an integer,
        with Monday as 1 through Sunday as 7.
        """
        weekday_num = self.datetime_now.isoweekday()
        return weekday_num

    def build_query(self):
        """
        Formats the query in SoQL. Attaching the returned string to the
        base_url will form an API query.
        https://dev.socrata.com/docs/queries/
        """
        words_dictionary = {
            'selection_fields': ", ".join(self.select_fields),
            'time_between': "{0} BETWEEN start24 AND end24".format(self._format_time())
        }

        query_url = (
            "?$select={selection_fields}"
            "&$where={time_between} AND dayorder={0}"
            "&$order=applicant ASC"
            "&$limit={1}"
            "&$offset={2}").format(
                                   self._get_weekday(),
                                   self.num_of_results,
                                   self.offset,
                                   **words_dictionary
                                   )

        return query_url
