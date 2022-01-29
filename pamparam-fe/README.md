
## Available Scripts

In the project directory, you can run:

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.


### `yarn start-api`

Runs the flask backend in the development mode.\
Open [http://localhost:5000](http://localhost:5000) to view it in the browser.

## Note:

In windows systems, SSL certificates may result in a discrepency when running the frontend server. You can bypass this problem by:

### export SET NODE_OPTIONS=--openssl-legacy-provider

You can add this line to the "start" script string in package.json file.\
