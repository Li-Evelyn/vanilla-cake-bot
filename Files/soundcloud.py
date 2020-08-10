import soundcloud

# TODO: add soundcloud link processing once https://soundcloud.com/you/apps/new opens up :(

client = soundcloud.Client(client_id="")
track_url = ""
track = client.get('/resolve', url=track_url)
print(track)
