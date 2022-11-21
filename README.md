# fringescrape

The following code will scrape the images and json from the "Void" location (default) and write them locally.
It will then create a csv file containing the drifter ids and traits from the "Void" location (default) 

```
from fringescrape import Fringescrape

csv_path = 'void_traits_3.csv' #This is were the drifter traits get written. I increment the number each time, but you don't have to.
fringe_scrape = Fringescrape()
fringe_scrape.scrape()
fringe_scrape.write_csv(csv_path)
```