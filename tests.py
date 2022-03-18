import datetime as dt
import json
import unittest

import jsonparser
import statscalculator


def get_answers() -> dict:
    """Get answers."""
    answers = None
    with open("test_answers.json", "r") as f:
        answers_data = f.read().encode()
        answers = json.loads(answers_data)
    return answers


def get_tests() -> dict:
    """Get tests."""
    tests = None
    with open("test_data.json", "r") as f:
        tests_data = f.read().encode()
        tests = json.loads(tests_data)
    return tests


def get_data() -> dict:
    """Get tests."""
    tests_data = None
    with open("test_data.json", "r") as f:
        tests_data = f.read().encode()
    return tests_data


class TestAll(unittest.TestCase):
    def test_jsonparser_getters(self):
        cases = [
            "12.05.18 00:00", "12.05.18 01:00"
            ]
        count = 0
        date = None
        parser = jsonparser.JSONParser(get_data(), "test_6_jsonparser", 0, 0)

        # check date getter
        for case in cases:
            with self.subTest(x="Date getter"):
                if count == 0:
                    date = parser.get_date(0, True)
                    self.assertEqual(date, dt.datetime.strptime(case, '%d.%m.%y %H:%M'))

                else:
                    date = parser.get_date(0, False)
                    self.assertEqual(date, dt.datetime.strptime(case, '%d.%m.%y %H:%M'))
            count += 1

        # check number of flights getter
        num_of_flights = len(get_answers()["test_6"])
        with self.subTest(x="Flights num getter"):
            flights = parser.get_num_of_flights()
            self.assertEqual(flights, num_of_flights)

        # check duration getter
        answer_duration = 3600
        with self.subTest(x="Duration getter"):
            duration = parser.get_duration(0)
            self.assertEqual(dt.timedelta(seconds=duration), dt.timedelta(seconds=answer_duration))

    def test_stats_avg_zero(self):
        parser = jsonparser.JSONParser(get_data(), "test_1_avg_0", 0, 0)
        stats_calc = statscalculator.StatsCalculator()
        for i in range(parser.get_num_of_flights()):
            stats_calc.add(parser.get_duration(i))
        stats_calc.calculate(90)

        answers = get_answers()['test_1']
        answers_avg = dt.datetime.strptime(answers[0]['average'], '%H:%M')
        answers_percentile = dt.datetime.strptime(answers[0]['percentile_90'], '%H:%M')

        with self.subTest(x="Checking average and percentile for 0 values"):
            avg, percentile = stats_calc.get_results()
            self.assertEqual(avg, dt.timedelta(hours=answers_avg.hour, minutes=answers_avg.minute))
            self.assertEqual(percentile, dt.timedelta(hours=answers_percentile.hour, minutes=answers_percentile.minute))

    def test_stats_avg_const(self):
        parser = jsonparser.JSONParser(get_data(), "test_2_avg_const", 0, 0)
        stats_calc = statscalculator.StatsCalculator()
        for i in range(parser.get_num_of_flights()):
            stats_calc.add(parser.get_duration(i))
        stats_calc.calculate(90)

        answers = get_answers()['test_2']
        answers_avg = dt.datetime.strptime(answers[0]['average'], '%H:%M')
        answers_percentile = dt.datetime.strptime(answers[0]['percentile_90'], '%H:%M')

        with self.subTest(x="Checking average and percentile for constant values"):
            avg, percentile = stats_calc.get_results()
            self.assertEqual(avg, dt.timedelta(hours=answers_avg.hour, minutes=answers_avg.minute))
            self.assertEqual(percentile, dt.timedelta(hours=answers_percentile.hour, minutes=answers_percentile.minute))

    def test_stats_avg_increase(self):
        parser = jsonparser.JSONParser(get_data(), "test_3_avg_const_increasing", 0, 0)
        stats_calc = statscalculator.StatsCalculator()
        for i in range(parser.get_num_of_flights()):
            stats_calc.add(parser.get_duration(i))
        stats_calc.calculate(90)

        answers = get_answers()['test_3']
        answers_avg = dt.datetime.strptime(answers[0]['average'], '%H:%M')
        answers_percentile = dt.datetime.strptime(answers[0]['percentile_90'], '%H:%M')

        with self.subTest(x="Checking average and percentile for increasing values"):
            avg, percentile = stats_calc.get_results()
            self.assertEqual(avg, dt.timedelta(hours=answers_avg.hour, minutes=answers_avg.minute))
            self.assertEqual(percentile, dt.timedelta(hours=answers_percentile.hour, minutes=answers_percentile.minute))

    def test_stats_avg_decrease(self):
        parser = jsonparser.JSONParser(get_data(), "test_4_avg_const_decreasing", 0, 0)
        stats_calc = statscalculator.StatsCalculator()
        for i in range(parser.get_num_of_flights()):
            stats_calc.add(parser.get_duration(i))
        stats_calc.calculate(90)

        answers = get_answers()['test_4']
        answers_avg = dt.datetime.strptime(answers[0]['average'], '%H:%M')
        answers_percentile = dt.datetime.strptime(answers[0]['percentile_90'], '%H:%M')

        with self.subTest(x="Checking average and percentile for decreasing values"):
            avg, percentile = stats_calc.get_results()
            self.assertEqual(avg, dt.timedelta(hours=answers_avg.hour, minutes=answers_avg.minute))
            self.assertEqual(percentile, dt.timedelta(hours=answers_percentile.hour, minutes=answers_percentile.minute))

    def test_stats_timezones(self):
        parser = jsonparser.JSONParser(get_data(), "test_5_timezones", 0, -1)
        stats_calc = statscalculator.StatsCalculator()
        for i in range(parser.get_num_of_flights()):
            stats_calc.add(parser.get_duration(i))
        stats_calc.calculate(90)

        answers = get_answers()['test_5']
        answers_avg = dt.datetime.strptime(answers[0]['average'], '%H:%M')
        answers_percentile = dt.datetime.strptime(answers[0]['percentile_90'], '%H:%M')

        with self.subTest(x="Checking values for timezone UTC and UTC(-1) for 2 hours flight"):
            avg, percentile = stats_calc.get_results()
            self.assertEqual(avg, dt.timedelta(hours=answers_avg.hour, minutes=answers_avg.minute))
            self.assertEqual(percentile, dt.timedelta(hours=answers_percentile.hour, minutes=answers_percentile.minute))


unittest.main()



