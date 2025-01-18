import geocoder
import webbrowser

def get_current_gps_coordinates():
    g = geocoder.ip('me')
    if g.latlng is not None: 
        return g.latlng
    else:
        return None

if __name__ == "__main__":
    coordinates = get_current_gps_coordinates()
    if coordinates is not None:
        latitude, longitude = coordinates
        print(f"Your current GPS coordinates are:")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")

        # a Google Maps URL with the coordinates
        maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"

        # Open the URL in the default web browser
        webbrowser.open(maps_url)
        print(f"Opening your location in Google Maps: {maps_url}")
    else:
        print("Unable to retrieve your GPS coordinates.")
