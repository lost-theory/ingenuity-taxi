'''
Basic ride cost calculator.
'''

LITERS_TO_GALLONS = 0.264172
KM_TO_MILES = 0.621371

MAINT_COST_PER_MILE = 0.29
CURRENT_FUEL_COST = 3.928 #http://www.sanfrangasprices.com/

def calc(f):
    xs = [x.strip().replace(" ", "").split(',') for x in open(f).readlines()]
    odos = [x for x in xs if x[1] == "odometer"]
    fuels = [x for x in xs if x[1] == "fuel_consumed_since_restart"]
    start, end = odos[0], odos[-1]
    start = float(start[2])
    end = float(end[2])
    miles_driven = (end - start) * KM_TO_MILES

    start,end = fuels[0], fuels[-1]
    start = float(start[2])
    end = float(end[2])
    gallons_used = (end - start) * LITERS_TO_GALLONS

    return miles_driven, gallons_used

if __name__ == "__main__":
    import sys
    sys.argv.pop(0)
    f = sys.argv.pop(0)

    miles_driven, gallons_used = calc(f)

    print "miles:", miles_driven
    print "gallons:", gallons_used

    fuel_cost = gallons_used * CURRENT_FUEL_COST
    maint_cost = miles_driven * MAINT_COST_PER_MILE

    print "fuel cost:", fuel_cost
    print "maint cost:", maint_cost

    print "total:", fuel_cost + maint_cost
