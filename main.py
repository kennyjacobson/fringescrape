from fringescrape import Fringescrape

csv_path = 'void_traits_3.csv' #This is were the drifter traits get written. I increment the number each time, but you don't have to.
fringe_scrape = Fringescrape()
fringe_scrape.scrape()
fringe_scrape.write_csv(csv_path)
fringe_scrape.write_combine_void('void_combined.csv', [csv_path, "void_traits_back.csv"])

# csv_path = 'void_traits_back.csv' #This is were the drifter traits get written. I increment the number each time, but you don't have to.
# fringe_scrape = Fringescrape('void_back')
# fringe_scrape.scrape()
# fringe_scrape.write_csv(csv_path)
