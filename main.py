import jsonparser
import statscalculator

TIME_ZONE_DEPARTURE = 0
TIME_ZONE_ARRIVAL = 0


def main():
    with open('tickets.json', 'r', encoding='utf-8') as f:
        data = f.read().encode()
        parser = jsonparser.JSONParser(data, "tickets", TIME_ZONE_DEPARTURE, TIME_ZONE_ARRIVAL)
        stats_calc = statscalculator.StatsCalculator()

        for i in range(parser.get_num_of_flights()):
            stats_calc.add(parser.get_duration(i))
        stats_calc.calculate(90)

        average_time, percentile_time = stats_calc.get_results()

        print(f"Average time is {average_time}")
        print(f"90th percentile of flight time is {percentile_time}")


if __name__ == "__main__":
    main()