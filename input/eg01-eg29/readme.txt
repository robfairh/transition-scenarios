readme:

eg01-eg29-flatpower-d3ploy.xml
deploys reactors with d3ploy
works

eg01-eg29-flatpower-d3ploy3.xml
deploys everything but the mixers
works

eg01-eg29-flatpower-d3ploy4.xml
deploys everything
doesn't work

nond3ploy-simple.xml
Has a case very similar to eg01-eg23
it deploys lwr and transitions to frs
mixer is complete has lwr/fr pu/u
works

d3ploy-simple1.xml
deploys just sinks using d3ploy
this is to check that d3ploy works for this input
works

next case deploys just mixer
mixer is complete has lwr/fr pu/u
this won't work
d3ploy-simple2.xml
it worked lol, but it worked poorly
it still records that the capacity for lwrpu is 0