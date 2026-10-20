# AI Persona
You're a senior software architect and should have a strong SOLID principle for web app development. 

# Application Background
I want to have a cycling tracking and planning web application written in html, csstailwind, and script. Choose which is best, if vanila, jquery, or anything you think it's better. Make sure that this is mobile friendly application as the will run mostly in mobile browser. I should have a button to enter in full screen mode. Remember to use OpenStreetMap

# Panels
This app is a map centric so it would be great to see things in a floating panels. Floating panels should be collapsible and expandable. When collapsed it will show a circular button on the map where I can click to show in expanded state. Make sure the panel collapse button is not overlapping the main controls

# Route Planner Panel
I should have a way to enter point A and point B and when I enter the locations, it should show the suggested address where I can select. I should also have a way to just select my starting and ending points on the map by tapping or clicking on the map for the start and end. 
- There should be a Check Route button to start the planning and should show the Dashboard at the bottom
- A button showing the advance planner

# Advance Route Planner Panel. 
Advance planner means I should be able to plan my speed on each section from point A to point B.
- I should have a way to add a desired speed on my selected section from the track. So probably add a button for adding a section? By default, a section starts from point A to point B and have a default speed which is 25km/h

# Dashboard Panel
- A sections where I can see my Current Speed and Average Speed.
- Moving time section and ride time section.
- Ride time section means, regardless if I stopped or riding, it will still be counted.
- Moving time means, it will only start the timer, if I am moving. It will stop the timer, if I stopped.
- An estimated time of arrival based on the advance route planner panel
- An elevation profile graph that uses open-elevation API
- There should be a button for Start, Pause, Stop, or Finish
- I should also see the sections I entered on advance route planner.

# Elevation Profile Graph
- I can drag my finger or mouse cursor on the graph and it will the exact point on the map. Make sure the marker is different against my current location
- I should be also able to zoom in or out on the graph and when zoomed in, I should be able to pan left and right.
- Make sure the graph is accurate as much as possible.

# Ride Starts
- If I started riding, elevation profile should also be aware of my current location so it should show a unique marker on the graph.
- The map should always be in "Heads Up" just like driving. It stays on north.