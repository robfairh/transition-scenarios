readme:

- eg01-eg29-flatpower-d3ploy.xml
deploys reactors with d3ploy
works

- eg01-eg29-flatpower-d3ploy3.xml
deploys everything but the mixers
works

- eg01-eg29-flatpower-d3ploy4.xml
deploys everything
doesn't work

- nond3ploy-simple.xml
Has a case very similar to eg01-eg23
it deploys lwr and transitions to frs
mixer is complete has lwr/fr pu/u
works

- d3ploy-simple1.xml
deploys just sinks using d3ploy
this is to check that d3ploy works for this input
works

next case deploys just mixer
mixer is complete has lwr/fr pu/u
this won't work
- d3ploy-simple2.xml
it worked lol, but it worked poorly
it still records that the capacity for lwrpu is 0

- d3ploy-simple3.xml
deploys just frmixer with d3ploy
mixer is not complete has lwrpu but not frpu
it records that the capacity for lwrpu is 3000
this is good

using installed capacity for d3ploy-simple2.xml
it works!!

- eg01-eg29-flatpower-d3ploy4.xml
it works with installed capacity!!
I am not sure it works awesomely well
The capacity is 2.4e4 when there are 1 frmixer and 3 moxmixers ...

- eg01-eg29-flatpower-d3ploy5.xml
Let's implement it better, there will be a frmixer1
deployed by lwrpy supply, same for a moxmixer1
Then there will be a frmixer2 deployed by the frpu supply
and there will be a moxmixer2 deployed by the moxpu supply
It doesn't work, the preference was set to 1000
I changed it to 1200, it got worse ... let's go back to 1000
Change mixing ratios ...

- d3ploy-simple4.xml
deploys just frmixer and moxmixer that uses lwrpu
mixers are complete
it doesn't work, same issue as with eg01-eg29

- eg01-eg29-flatpower-d3ploy4.xml
it works well now with the PR in cycamore and the PR in d3ploy
both for installed capacity and predicted capacity

- d3ploy-simple4.xml
It should be working now!
Solver minimizes the oversupply and also the number of facilities deployed.

- eg01-eg29-flatpower-d3ploy5.xml
Trying with new cycamore and d3ploy.
It is necessary to play around with the sizes of the buffers.
Both mixers should have in total something close to the supply of the driving commodity
for ex: lwrpu. If the supply is 21000, then one could have 13000 and the other one 8000