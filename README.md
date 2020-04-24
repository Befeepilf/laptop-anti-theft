# AntiTheft

This python script accesses the camera of your laptop and takes snapshots whenever a face is detected in the current image. These snapshots are stored in a Firestore database for the case that the laptop was stolen.

### Requirements
- A laptop with a camera
- Python3
- `pip install opencv-python numpy google-cloud-storage google-cloud-firestore`
- A Firestore database
- A Firebase service account key allowing access to this database
- The environment variable `GOOGLE_APPLICATION_CREDENTIALS` set to the path of the service account key (https://cloud.google.com/docs/authentication/getting-started)


### Usage
- Simply run the script
- To terminate properly focus the preview window and press ESC. The script then stops recording and waits for remaining snapshots to be uploaded to the database. 
