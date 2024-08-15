# Video Generator for Suicide Prevention Training

This guide will help you run the Video Generator application using Docker Desktop.

## Prerequisites

1. Install Docker Desktop:
   - For Windows or Mac: Download and install from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - For Linux: Follow the instructions for Docker Engine at [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

2. Make sure Docker Desktop is running on your computer.

## Running the Application

1. Open Docker Desktop
   - On Windows: You can find it in the Start menu
   - On Mac: You can find it in the Applications folder or the menu bar

2. Open a terminal or command prompt:
   - On Windows: Press Win+R, type "cmd", and press Enter
   - On Mac: Open the Terminal app from Applications > Utilities
   - On Linux: Use your preferred terminal application

3. In the terminal, copy and paste the following command, then press Enter:

docker run -p 5000:5000 nilshuysmans/suicide-prevention-video-generator

4. Wait for the message that says the application is running. This might take a few minutes the first time.

5. Open your web browser and go to: [http://localhost:5000](http://localhost:5000)

You should now see the Video Generator interface in your web browser.

## Using the Application

1. Select two characters from the dropdown menus.

2. Choose a background scene.

3. Add dialogue entries:
- Click the '+' button to add a new dialogue entry.
- For each entry, type what each character says and choose their emotion.

4. Click "Generate Video" when you're done adding dialogues.

5. Wait for the video to generate. This may take a few moments.

6. Once complete, the video will automatically play in your browser. You can save it by right-clicking and selecting "Save video as...".

## Stopping the Application

When you're done using the application:

1. Go back to the terminal or command prompt where you ran the docker command.
2. Press Ctrl+C to stop the application.
3. You can close the terminal and Docker Desktop if you don't plan to use it again soon.

## Troubleshooting

- If you see an error message or the page doesn't load, try refreshing your browser.
- If the application still doesn't work, try these steps:
1. In Docker Desktop, go to the "Containers" tab.
2. Find the container named "nilshuysmans/suicide-prevention-video-generator", click the stop button (square icon).
3. After it stops, click the delete button (trash can icon).
4. Run the docker command from step 3 of "Running the Application" again.

