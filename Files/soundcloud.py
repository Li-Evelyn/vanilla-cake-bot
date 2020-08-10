import soundcloud

client = soundcloud.Client(client_id="")
track_url = ""
track = client.get('/resolve', url=track_url)
print(track)