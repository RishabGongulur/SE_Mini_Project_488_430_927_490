import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
SPOTIPY_CLIENT_ID = '38e2c5e1ae6b4d5088579d468d8a0379'
SPOTIPY_CLIENT_SECRET = 'af3ab5d6e9ac4026b5a35751a663a643'

# Spotipy setup
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                                         client_secret=SPOTIPY_CLIENT_SECRET))

# Streamlit app
st.title('Spotify Artist Dashboard')
option = st.sidebar.selectbox("Select one of the following:", ("Search for an Artist", "Search for a Track"))

if option == "Search for an Artist":
    # Artist search
    artist_name = st.text_input('Enter Artist Name:')
    if artist_name:
        try:
            results = sp.search(q=artist_name, type='artist', limit=1)
            if results['artists']['items']:
                artist = results['artists']['items'][0]

                # Display artist image in the sidebar
                st.sidebar.subheader('Artist Information')
                if artist['images']:
                    st.sidebar.image(artist['images'][0]['url'], caption=artist['name'], use_column_width=True)  # Adjust the width as needed
                st.sidebar.write(f'Followers: {artist["followers"]["total"]}')
                st.sidebar.write(f'Genres: {", ".join(artist["genres"])}')

                # Display top tracks without a dropdown
                st.subheader("Top Tracks")
                top_tracks = sp.artist_top_tracks(artist['id'])
                for idx, track in enumerate(top_tracks['tracks'][:5]):  # Limit to top 5 tracks
                    st.write(f"{idx + 1}. {track['name']}")

                # Display album information in a collapsible dropdown
                with st.expander("Album Information"):
                    # Display the top 3 albums
                    top_albums = sp.artist_albums(artist['id'], album_type='album', limit=3)
                    columns_albums = st.columns(3)
                    for column, album in zip(columns_albums, top_albums['items']):
                        with column:
                            st.write(f"**[{album['name']}]({album['external_urls']['spotify']})**")  # Display album name as a clickable link
                            st.image(album['images'][0]['url'], caption=album['name'], width=150)  # Adjust the width as needed
                            st.write(f"Release Date: {album['release_date']}")

                            # Display top 5 tracks from the album without dots
                            st.write("Top Tracks:")
                            album_tracks = sp.album_tracks(album['id'])
                            for idx, track in enumerate(album_tracks['items'][:5]):
                                st.write(f"{idx + 1}. {track['name']}")

                with st.expander("Related Artists"):
                    related_artists = sp.artist_related_artists(artist['id'])
                    columns_related = st.columns(3)
                    for column, related_artist in zip(columns_related, related_artists['artists']):
                        with column:
                            st.write(related_artist['name'])

            else:
                st.warning('Artist not found. Please enter a valid artist name.')

        except Exception as e:
            st.error(f"An error occurred: {e}")

    

elif option == "Search for a Track":
    track_name = st.text_input('Enter Track Name:')
    if track_name:
        try:
            results = sp.search(q=track_name, type='track', limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]

                # Create two columns: one for the main track information and one for the related tracks
                track_info_column, related_tracks_column = st.columns([2, 1])

                # Display track information in the first column
                with track_info_column:
                    st.subheader("Track Information")
                    st.image(track['album']['images'][0]['url'], caption=track['album']['name'], width=150)
                    st.write(f"Name: [{track['name']}]({track['external_urls']['spotify']})")
                    st.write(f"Artists: {', '.join([artist['name'] for artist in track['artists']])}")
                    st.write(f"Album: {track['album']['name']}")
                    st.write(f"Release Date: {track['album']['release_date']}")
                    st.write(f"Popularity: {track['popularity']}")

                    # Display the song preview
                    if 'preview_url' in track and track['preview_url']:
                        st.audio(track['preview_url'], format='audio/ogg', start_time=0)

                # Display related tracks in the second column on the main page
                with related_tracks_column:
                    st.subheader("Related Tracks on the Main Page")
                    # Get related tracks
                    related_tracks = sp.recommendations(seed_tracks=[track['id']], limit=5)['tracks']
                    
                    # Display related tracks information with images and links
                    for idx, related_track in enumerate(related_tracks):
                        st.write(f"{idx + 1}. [{related_track['name']}]({related_track['external_urls']['spotify']}) - {', '.join([artist['name'] for artist in related_track['artists']])}")
                        st.image(related_track['album']['images'][0]['url'], caption=related_track['album']['name'], width=100)

            else:
                st.warning('Track not found. Please enter a valid track name.')

        except Exception as e:
            st.error(f"An error occurred: {e}")
