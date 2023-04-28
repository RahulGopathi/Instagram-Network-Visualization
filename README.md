# My-Instagram-Network

Visualization of the instagram network using Login credentials of the user's instagram profile.

GitHub repository Link: https://github.com/RahulGopathi/Instagram-Network-Visualization.git

### Procedure for visualizing Instagram network

- Install [python](https://www.python.org/downloads/) in your environment and clone the reporsitory using following command

```
git clone https://github.com/RahulGopathi/Instagram-Network-Visualization.git
```

- Create a new virtual environment and activate it using the following command

```
python -m venv env
.\env\Scripts\activate
```

- If you have conda installed locally, you can run install dependencies from `requirements.txt`

```
conda create --name env --file requirements.txt
```

Install the dependencies with python-pip

```
pip install -r requirements_pip.txt
```

- Navigate to the “scraping” folder that contains the scripts. You can run the first script using this command:

```
python get_my_followers.py --username your_IG_username\
                             --password your_IG_password
```

- After executing the above command, "my_followers.txt" file will be created in the current directory.

- Execute the below command which makes use of the output of the first script and saves the relations in `relations.txt`.

```
python get_relations.py --username your_IG_username\
                          --password your_IG_password\
                          --relations_file relations.txt
```

- After running the above command, the program would have scraped all the profiles and you’ll end up with a `relations.txt` file containing all the relations

```
python relations_to_json.py --username your_IG_username\
                              --input_txt_file relations.txt\
                              --output_json_file relations.json\
```

- Replace the `relations.json` file in "visual" folder with the `relations.json` file generated in the "scraping" folder.

- Open the `index.html` file present in the "visual" folder in the browser using any Live server (for example, VS Code "Live server" Extention)

- It will open the instagram network containing the nodes representing users and the edges representing relation between them.

- Then in your terminal, navigate to the “analysis” folder and run:

```
python global_analysis.py --username your_IG_username\
                            --input_txt_file path_to_relations.txt\
```

- By executing the above command you will get the following statistics about your network:
- **Density** : This metric tells you how dense the network is.
- **Degree** : This property tells us how many edges are connected to a node by reporting the average in degree and out degree of the network.
- It also crates a plot in the same directory which shows the degree distribution in the network.

- In the same directory, run the following command to view the local level analysis

```
python local_analysis.py --username your_IG_username\
                           --input_txt_file path_to_relations.txt\
```

- The above command will give the statistics about Betweenness centrality, Closeness centrality, Degree centrality and other statistics.
