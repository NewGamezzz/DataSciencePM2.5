from utils.base import *

class ScrapInterface:
  def scraping(self, driver, **kwargs) -> any:
    raise NotImplemented

class ScrapWind(ScrapInterface):
  def scraping(self, driver, startDate=None, stopDate=None, location=None, basepath=None, savepath=None):
    N = len(location)
    position = {"BKK": (100.536443, 13.729984), 
            "Chiangmai": (98.969661, 18.840633),
            "Khonkaen": (102.835251, 16.445329),
            "Rayong": (101.275875, 12.671521),
            "Saraburi": (100.871996, 14.685833),
            "Surat": (99.325355, 9.126057)}
    wind_direction = [[] for i in range(N)]
    wind_speed = [[] for i in range(N)]
    date_time = [[] for i in range(N)]
    UTC_startDate = startDate - timedelta(hours=7)

    Year = str(UTC_startDate.year)
    Month = str(UTC_startDate.month).zfill(2)
    Date = str(UTC_startDate.day).zfill(2)
    Time = str(UTC_startDate.hour).zfill(2) + str(UTC_startDate.minute).zfill(2)

    long, lat = position[location[0]]
    url = f'https://earth.nullschool.net/#{Year}/{Month}/{Date}/{Time}Z/wind/isobaric/850hPa/loc={long},{lat}'
    driver.get(url)

    time.sleep(10)
    element = driver.find_element(By.ID, 'menu')
    driver.execute_script('arguments[0].removeAttribute("hidden")', element)
    element = driver.find_element(By.ID, 'spotlight-panel')
    driver.execute_script('arguments[0].removeAttribute("hidden")', element)
    time.sleep(10)

    iter = 0
    while True:
      try: # <-- try to scrap, if can't refresh page again then scrap
        status = 'Downloading'
        while status == 'Downloading':
          soup = BeautifulSoup(driver.page_source, 'lxml')
          status = soup.find('div', {'data-name': 'status-card', 'class': 'vert-unchanged row card'}).select_one('div.field')
        
        

        for idx, loc in enumerate(location):
          longtitude, latitude = position[loc]
          cur_url = driver.current_url
          new_url = cur_url.split('loc=')[0:1]
          new_url.append(str(longtitude)+','+str(latitude))
          new_url = 'loc='.join(new_url)
          driver.get(new_url)
          soup = BeautifulSoup(driver.page_source, 'lxml')

          wind = soup.find('div', {'data-name': 'spotlight-a', 'class': 'vert-unchanged row'}).select_one('div').text.split(' @ ')
          wind = tuple(map(lambda x: float(re.sub('[^0-9.]', '', x)), wind))

          local_time = soup.find('div', {'data-name': 'date-field'}).text
          local_time = datetime.strptime(local_time, '%Y-%m-%d %H:%M Local')

          wind_direction[idx].append(wind[0])
          wind_speed[idx].append(wind[1])
          date_time[idx].append(local_time.strftime('%Y-%m-%d %H:%M'))
        
        if local_time > stopDate:
          for idx, loc in enumerate(location):
            df = pd.DataFrame({'date_time': date_time[idx], 
                  'wind speed': wind_speed[idx], 'wind direction': wind_direction[idx]}).drop_duplicates()
            result_path = os.path.join(basepath, loc)
            result_path = os.path.join(result_path, savepath)
            df.to_csv(result_path, index=False)
          break


        iter += 1
        
        if iter % 10 == 0:
          clear_output(wait=True)
          print("DateTime:", local_time)
          for idx, loc in enumerate(location):
            df = pd.DataFrame({'date_time': date_time[idx], 
                  'wind speed': wind_speed[idx], 'wind direction': wind_direction[idx]}).drop_duplicates()
            result_path = os.path.join(basepath, loc)
            result_path = os.path.join(result_path, savepath)
            df.to_csv(result_path, index=False)

        next_button = driver.find_element(By.XPATH, "//button[@data-name='nav-next1']")
        next_button.click()
        time.sleep(2)
      except: 
        driver.refresh()
        time.sleep(2)
        element = driver.find_element(By.ID, 'menu')
        driver.execute_script('arguments[0].removeAttribute("hidden")', element)
        element = driver.find_element(By.ID, 'spotlight-panel')
        driver.execute_script('arguments[0].removeAttribute("hidden")', element)
        time.sleep(2)
        continue

      

    # df = pd.DataFrame({'date_time': date_time, 
    #              'wind speed': wind_speed, 'wind direction': wind_direction})
    # return df.drop_duplicates()

class ScrapTemperature(ScrapInterface):
  def scraping(self, driver, startDate=None, stopDate=None, location=None, basepath=None, savepath=None):
    N = len(location)
    position = {"BKK": (100.536443, 13.729984), 
            "Chiangmai": (98.969661, 18.840633),
            "Khonkaen": (102.835251, 16.445329),
            "Rayong": (101.275875, 12.671521),
            "Saraburi": (100.871996, 14.685833),
            "Surat": (99.325355, 9.126057)}
    temperature = [[] for i in range(N)]
    date_time = [[] for i in range(N)]
    UTC_startDate = startDate - timedelta(hours=7)

    Year = str(UTC_startDate.year)
    Month = str(UTC_startDate.month).zfill(2)
    Date = str(UTC_startDate.day).zfill(2)
    Time = str(UTC_startDate.hour).zfill(2) + str(UTC_startDate.minute).zfill(2)

    long, lat = position[location[0]]
    url = f'https://earth.nullschool.net/#{Year}/{Month}/{Date}/{Time}Z/wind/surface/level/overlay=temp/loc={long},{lat}'
    driver.get(url)

    time.sleep(10)
    element = driver.find_element(By.ID, 'menu')
    driver.execute_script('arguments[0].removeAttribute("hidden")', element)
    element = driver.find_element(By.ID, 'spotlight-panel')
    driver.execute_script('arguments[0].removeAttribute("hidden")', element)
    time.sleep(10)

    iter = 0
    while True:
      try: # <-- try to scrap, if can't refresh page again then scrap
        status = 'Downloading'
        while status == 'Downloading':
          soup = BeautifulSoup(driver.page_source, 'lxml')
          status = soup.find('div', {'data-name': 'status-card', 'class': 'vert-unchanged row card'}).select_one('div.field')
        
        

        for idx, loc in enumerate(location):
          longtitude, latitude = position[loc]
          cur_url = driver.current_url
          new_url = cur_url.split('loc=')[0:1]
          new_url.append(str(longtitude)+','+str(latitude))
          new_url = 'loc='.join(new_url)
          driver.get(new_url)
          soup = BeautifulSoup(driver.page_source, 'lxml')

          temp = soup.find('div', {'data-name': 'spotlight-b', 'class': 'vert-unchanged row'}).select_one('div').text.split(' @ ')
          temp = tuple(map(lambda x: float(re.sub('[^0-9.]', '', x)), temp))

          local_time = soup.find('div', {'data-name': 'date-field'}).text
          local_time = datetime.strptime(local_time, '%Y-%m-%d %H:%M Local')

          temperature[idx].append(temp)
          date_time[idx].append(local_time.strftime('%Y-%m-%d %H:%M'))
        
        if local_time > stopDate:
          for idx, loc in enumerate(location):
            df = pd.DataFrame({'date_time': date_time[idx], 'temp': temperature[idx]}).drop_duplicates()
            result_path = os.path.join(basepath, loc)
            result_path = os.path.join(result_path, savepath)
            df.to_csv(result_path, index=False)
          break


        iter += 1
        
        if iter % 10 == 0:
          clear_output(wait=True)
          print("DateTime:", local_time)
          for idx, loc in enumerate(location):
            df = pd.DataFrame({'date_time': date_time[idx], 'temp': temperature[idx]}).drop_duplicates()
            result_path = os.path.join(basepath, loc)
            result_path = os.path.join(result_path, savepath)
            df.to_csv(result_path, index=False)

        next_button = driver.find_element(By.XPATH, "//button[@data-name='nav-next1']")
        next_button.click()
        time.sleep(2)
      except: 
        driver.refresh()
        time.sleep(2)
        element = driver.find_element(By.ID, 'menu')
        driver.execute_script('arguments[0].removeAttribute("hidden")', element)
        element = driver.find_element(By.ID, 'spotlight-panel')
        driver.execute_script('arguments[0].removeAttribute("hidden")', element)
        time.sleep(2)
        continue

      

    # df = pd.DataFrame({'date_time': date_time[idx], 'temp': temperature[idx]})
    # return df.drop_duplicates()