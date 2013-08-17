'''
Interactive display of (time, odometer, fuel, cost), e.g.:

$ python interactive.py data/bb_c-max_day_1_part_1.csv
t=0.0   odo=0.0 fuel=0.0    cost=0.0
t=5.00454115868 odo=0.0254855315666 fuel=0.0    cost=0.100107167993
t=10.0005161762 odo=0.0254855315666 fuel=0.0    cost=0.100107167993
t=14.9398450851 odo=0.0254855315666 fuel=0.0    cost=0.100107167993
t=20.0050661564 odo=0.0254855315666 fuel=0.0    cost=0.100107167993
t=24.996628046  odo=0.0254855315666 fuel=0.0    cost=0.100107167993
t=29.995401144  odo=0.0254855315666 fuel=0.0    cost=0.100107167993
t=35.0053191185 odo=0.0266996905002 fuel=0.0    cost=0.104876384285
t=40.0049920082 odo=0.0388356875    fuel=0.001783161    cost=0.159550836908
...
'''

import itertools

from rate import LITERS_TO_GALLONS, KM_TO_MILES, MAINT_COST_PER_MILE, CURRENT_FUEL_COST

TS, FIELD, VAL = range(3)

def generate_odo_fuel_pairs(stream, resolution=5):
    start = int(float(stream[0][0]))

    bucket = start - (start % resolution)
    current_odo = -1
    current_fuel = -1
    last_fuel = -1
    for row in stream:
        ts = float(row[TS])
        if row[FIELD] not in ["odometer", "fuel_consumed_since_restart"]:
            continue
        if current_odo == -1 and row[FIELD] == "odometer":
            current_odo = row[VAL]
        if current_fuel == -1 and row[FIELD] == "fuel_consumed_since_restart":
            current_fuel = row[VAL]
        if (ts - (ts % resolution)) > bucket:
            if current_odo > 0:
                #fuel does not start at 0 on some runs
                current_fuel = max(current_fuel, last_fuel)
                yield (ts, (float(current_odo), float(current_fuel)))
            bucket = (ts - (ts % resolution))
            current_odo = -1
            last_fuel = current_fuel
            current_fuel = -1

if __name__ == "__main__":
    import sys
    sys.argv.pop(0)
    f = sys.argv.pop(0)

    xs = [x.strip().replace(" ", "").split(',') for x in open(f).readlines()]

    pairs = generate_odo_fuel_pairs(xs)

    (t0, (odo0, fuel0)) = init = next(pairs)
    for (t, (odo, fuel)) in itertools.chain([init], pairs):
        t_now = (t - t0)
        odo_now = (odo - odo0) * KM_TO_MILES
        fuel_now = (fuel - fuel0) * LITERS_TO_GALLONS
        print "t=%s\todo=%s\tfuel=%s\tcost=%s" % (
            t_now, odo_now, fuel_now, (odo_now * CURRENT_FUEL_COST) + (fuel_now * CURRENT_FUEL_COST)
        )
        import time; time.sleep(0.2)
