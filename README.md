# How to configure IFTTT

1. Add a new applet
2. Pick "webhooks" as the service for "this"
3. Pick "Receive a web request" as the trigger
4. Enter "HdCChecker_price_down" when asked for the event name
5. Pick "notifications" as the service for "that"
6. Pick "Send a rich notification from the IFTTT app" as the action
7. Enter "HdCChecker" in the title 
8. Enter "Hotel's "{{Value1}}" room price went down from {{Value2}} {{Value3}} !" in the message
9. Save


## How to find the ifttt key

1. Go to the service category 
2. Look for "webhooks"
3. Go to settings
4. Your personal ifttt key is included in the url field (after "use/")
5. Copy your ifttt key in the configuration file "conf.json"