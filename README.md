ingenuity-taxi
==============

BoingBoing Ingenuity Hackday project: Taximeter

* OpenXC docs: http://boing-boing-fdc.github.io/
* Our notes: https://github.com/lost-theory/ingenuity-taxi/wiki/Notes
* Photos: https://github.com/lost-theory/ingenuity-taxi/wiki

Winner of Best Use of Data!

Idea
====

Show drivers the real-time cost of their trip (fuel & maintenance) using the
data from OpenXC.

Right now we are only looking at two fields: `odometer` and
`fuel_consumed_since_restart`. If we had more time, we could have looked at
acceleration, braking, tire pressure, etc. to get a more accurate rate.

Other ideas:

* apply this data to a ride-sharing program, where a large fleet of vehicles are shared and users are billed based on the rate calculated from the data
* use GPS information to determine the fuel cost for your current area
* use vehicle data to get a more accurate maintenance cost (SUV vs. hybrid, 2000 vs. 2013 model)

Results
=======

By parsing the ride CSVs and treating each CSV as a separate trip, we obtain the following:

* distance driven (miles)
* gallons of fuel used (gallons)

We combine that information with:

* the current fuel cost (per gallon)
* an estimated cost of running the vehicle (per mile), including:
  * insurance
  * maintenance (oil changes, tires, brakes)
  * depreciation

From that we get:

* total cost of trip = (distance * maint. cost per mile) + (gallons * fuel cost per gallon)

And display these values as new data comes in to two places (concurrently):

* an arduino with a 7-segment display attached (4 digits, e.g. $12.34)
* a desktop or mobile browser

This is done with a python app (server.py) using Tornado, pyserial, and
websockets.

Authors
=======

* Steven Kryskalla (github.com/lost-theory)
* David Harris (twitter.com/physicsdavid)
