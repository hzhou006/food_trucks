import unittest
from lib.query import QueryCurrentFoodTrucks

class TestQuery(unittest.TestCase):
    def test_open_food_trucks_url(self):
        """
        A quick test so I can view the query I've built easily.
        """
        url = QueryCurrentFoodTrucks(offset=0)
        time = url._format_time()
        day = url._get_weekday()
        expected_output = (
            "?$select=applicant, location"
            "&$where={0} BETWEEN start24 AND end24 AND dayorder={1}"
            "&$order=applicant ASC"
            "&$limit=10"
            "&$offset=0").format(time, day)

        output = url.build_query()
        print output
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
