#  THIS IS A SIMPLE FLASK APPLICATION THAT YOU CAN IMPROVE FOR BUS RIDE BOOKING

You can create a virtual environment and then install dependencies by running:

``` pip install -r requirements.txt ```

After wards yousetup the database, you can also make adjustments to the models.py and forms.py in the /app directory.

To initialise the database:

``` flask db init ```

To make your migrations and commit:

``` flask db migrate -m "Initial migration" ```

To finalise:

``` flask db upgrade ```

You start the application using:

``` flask run ```
