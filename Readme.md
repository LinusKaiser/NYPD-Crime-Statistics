<img src="Images/Compstat 2.0 Example.png"></img>

### Short Description
In the image above, we can see the Compstat 2.0 Website. On the left of the website, in the **CompStat Book** 
section, it can be specified what data points should be shown on the **Incident Map** in the middle. (In the 
image above, I selected the **<u>Total</u>** Number of Crimes that Happened in the **<u>Week to Date</u>** 
**<u>2022</u>** from 06/13/2022 - 06/19/2022). With each circle, there are relational x and y coordinates 
as well as a specific and broad cime label and the time of the occurrence of the crime. Each circle on the 
map has to be clicked individually to derive the previously mentioned data from the HTML code of the website.

### Objective
- first, specify a category and time frame of crimes that should be displayed on the map
- loop through all circles on the map to get the time, location, and specific/broad crime label


- there are two separate implementations that I have tried to make this happen 
    1. (**Traveling Salesperson Implementation**) zooming in on the map very closely to make sure no circles overlap each other to then move on the map via a NN traveling salesperson algorithm to every circle and then clicking it once it is in the visible frame of the map

    2. (**JavaScript Implementation**) zooming out on the map so that every circle is within the visible frame of the map and then hide all circles and make every circle appear after each other to avoid overlapping to then click them individually 

- I ended up choosing the 2. implementation as it's more practical. On the map are some circles that are very close together and even overlap when zooming in to the maximum, which would require another algorithm that works with `offsets` to derive the overlappings of those circles.

### In Planning

- database implementation
- parallel execution via multiple taps to increase scrapping speed
- data exploration
- data visualization
- machine-learning application

### 2022 Weekly Crimes in NYC
-----

![link](/Outputs/ezgif.com-gif-maker.gif)

-----