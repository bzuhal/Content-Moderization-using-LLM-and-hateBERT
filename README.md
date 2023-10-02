# AI Monitoring

Run the Project:

# before running the project you need to install 2 libs
 > pip install flask
 > pip install flask-restplus
 > pip install flasgger
 > pip install transformers
 > pip install prometheus_flask_exporter
 > pip install prometheus_client
 > pip install psutil

# to run django project use the following command
 > python task3.py

# now the application run in the following url:
 > http://127.0.0.1:5000/

# swagger doc will be in this url:
 > http://127.0.0.1:5000/apidocs/

In this Project you will monitor the requests

1. First you need to download <b>Prometheus</b> form this url <a href="https://prometheus.io/download/" target="_blank">(https://prometheus.io/download/)</a>

2. After downloading and extracting files <b>prometheus.yml</b> file inside project need to be opened and **scrape_configs** section be changed and detail of our flask app need to be added:
    ```
    scrape_configs:
        - job_name: 'my_flask_app'
        static_configs:
            - targets: ['127.0.0.1:5000']
    ```
    `http://127.0.0.1:5000/ is the address of our flask server`

3. After changing the config file open a command line inside <b>Prometheus</b> folder and run the following command:<br/>
    > prometheus.exe<br/>

   Now You are <b>Prometheus</b> is monitoring your flask application and you can check your <b>Prometheus</b> using the following URL:<br/>
    > http://localhost:9090/

4. Download <b>Grafana</b> for Creating Graphs and Monitoring <b>Prometheus</b>:
    > https://grafana.com/grafana/download

5. After downloading and Installing G now you can access this service using the following details:
    > http://localhost:3000 <br/>
    > username: **admin**<br/>
    > password: **admin**<br/>

6. After login in you need to create data source and connect with P as below:
    <h5>6.1 Log into Grafana:</h5>
    <p>
    Open your web browser and navigate to your Grafana instance (usually at http://localhost:3000).
    Log in with your Grafana credentials.
    </p>
    <h5>6.2 Access Data Sources:</h5>
    <p>
    Once logged in, click on the gear icon (⚙️) in the left sidebar to open the Configuration menu.
    Under "Data Sources," click on "Add data source."
    </p>
    <h5>6.3 Select Prometheus as the Data Source:</h5>
    <p>
    In the "Add data source" page, you'll see a list of available data sources. Search for "Prometheus" and click on it.
    </p>
    <h5>6.4 Configure the Prometheus Data Source:</h5>
    <p>
        You will be taken to the configuration page for the Prometheus data source. Configure the following settings:
    </p>
    <p>
        Name: Give your data source a name (e.g., "Prometheus").
        URL: Set the URL to your Prometheus server. By default, Prometheus runs on http://localhost:9090 unless you've configured it differently.
        Access: Choose how Grafana should access the Prometheus server. The default option, "Server (Default)," should work for most setups.
        Scrape Interval: This setting is optional and determines how often Grafana scrapes data from Prometheus. The default value is usually sufficient for most use cases.
        HTTP Method: Select "GET" or "POST" depending on your Prometheus server's configuration. "GET" is the default and should work for most setups.
    </p>
    <h5>6.5 Authentication (Optional): </h5>
    <p>
        If your Prometheus server is secured with basic authentication, you can provide the username and password under the "HTTP" section.
    </p>
    <h5>6.6 HTTP Settings (Optional): </h5>
    <p>
        You can customize additional HTTP settings if needed. However, the default settings should work in most cases.
    </p>
    <h5>6.7 Scrape Discovery (Optional): </h5>
    <p>
        If you want to use Prometheus service discovery for targets, you can enable this feature and configure it accordingly.
    </p>
    <h5> 6.8 Custom HTTP Headers (Optional):</h5>
    <p>
        You can add custom HTTP headers if required for your Prometheus setup.
    </p>
    <h5> 6.9 Save & Test: </h5>
    <p>
        After configuring the Prometheus data source, click the "Save & Test" button at the bottom of the page.
        Grafana will attempt to connect to your Prometheus server and test the data source. If everything is configured correctly, you should see a success message.
    </p>
    <h5> 6.10 Create Dashboards:</h5>
    <p>
    Now that you have connected Grafana to Prometheus, you can create dashboards and panels to visualize your Prometheus metrics. Click the "+" icon in the left sidebar to create a new dashboard and add panels to it.
    </p>
