<!DOCTYPE html>
<html>
    <head>
        <title>SARS-CoV-2 Protein Database</title>
        <link rel="stylesheet" type="text/css" href="Protein_DB.css" />
    </head>
    <body>
        <div id="Container">
                <div id="Navigation">
                    <a href="index.html">Title</a>
                    <a href="home_page.html">Home</a>
                    <a href="History_page.html">History</a>
                        <div class="dropdown">
                            <button class="dropbutton">Genetic Databases
                                <i class="fa fa-caret-down"></i>
                            </button>
                            <div class="dropdown_content">
                                <a class="selected" href="Pro_table.php">Protein Database</a>
                                <a href="DNA_Table.php">DNA Database</a>
                                <a href="PDB_table.php">PDB Database</a>
                                <a href="Ref_Seq.php">Reference Database</a>
                            </div>
                        </div>
                    <a href="3Dview.html">Protein Visualiser</a>
                    <a href="Global_stats.html">Global Statistics</a>
                    <a href="User_guide.html">User guide</a>
                    <a href="References.html">References</a>
                    <div id="Nav_line">
                        <hr />
                    </div>
                </div>
            <div id="Title">
                <h1>SARS-CoV-2 Protein Database</h1>
            </div>
            <div id="Sequence_list">
                <p>This is the section where the protein sequences are grouped by different ORF strains in a SQL database.</p>
                <hr />
                <!--Uses CountRows function described below-->
                <div id="Seq_count_button">
                    <h2>Sequence Counter<h2>
                    <input type="button" id="btnGetCount" value="Sequence count" onclick = "CountRows()" />
                </div>
                <hr />
                <div id="Pro_Seq_Title">
                    <h2>Find a Protein Sequence</h2>
                </div>
                <!--Uses table search function to find best match if any from HTML table-->
                <div class="Pro_search">
                    <form class="example">
                    <label for="MyInput">Search database by Release date or ORF number (Example: "2020-02-29" or "ORF3"):</label><br>
                        <input ID="myInput" type="text" placeholder="Search for proteins..." name="search"> 
                    </form>
                    <br />
                    <br />
                </div>
                <p>Below is the table that shows all SARS-CoV-2 protein sequences in the database:</p>
                <hr />
                <!--Table populated using MySQL table via PHP-->
                <table id="PHP_table">
                    <tr>
                        <th>Accession</th>
                        <th>Protein ID</th>
                        <th>ORF product</th>
                        <th>ORF FASTA</th>
                        <th>Release date</th>
                        <th>Reference</th>
                    </tr>
                    <?php
                    /*Assign login details as variables*/
                    $servername = "localhost";
                    $username = "lampuser";
                    $password = "changeme";
                    $dbName = "Covid_19";
                    
                    /*Create connection to MySQL database via PHP*/
                    $connection = mysqli_connect($servername,$username,$password,$dbName);
                    
                    /*Assigns MySQL command as variable*/
                    $sql_showtable = "select * from covid_proteins;";
                    $results = mysqli_query($connection, $sql_showtable);
                    
                    $resultsCheck = mysqli_num_rows($results);

                    /*If/While populates every row of HTML with MySQL data*/
                    if($resultsCheck>0){
                        while($row = mysqli_fetch_assoc($results)){
                            echo "<tr><td>". $row['ACCESSION']."\n". "</td><td>" .$row['PROTEIN_ID']."\n". "</td><td>" .$row['ORF_PRODUCT']."\n". "</td><td>" .$row['ORF_FASTA']."\n". "</td><td>" .$row['RELEASE_DATE']."\n". "</td><td>" .$row['REFERENCE']."<br/>". "</td></tr>";
                        }
                    }
                    ?>
                </table>
                <br />
                <br />
                <!--Counts the number of rows in the HTML table then outputs count-->
                <div id="Table_length_count">
                    <script type="text/javascript">
                        function CountRows() {
                            var totalRowCount = 0;
                            var rowCount = 0;
                            var table = document.getElementById("PHP_table");
                            var rows = table.getElementsByTagName("tr")
                            for (var i = 0; i < rows.length; i++) {
                                totalRowCount++;
                                if (rows[i].getElementsByTagName("td").length > 0) {
                                    rowCount++;
                                }
                            }
                            var message = "Protein Sequence Count: " + rowCount;
                            alert(message);
                        }
                    </script>
                </div>
                <!--Search bar function to searach all columns and rows for best match-->
                <div id="Table_search">
                    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                    <script>
                    $(document).ready(function(){
                    $("#myInput").on("keyup", function() {
                        var value = $(this).val().toLowerCase();
                        $("#PHP_table tr").filter(function() {
                        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
                        });
                    });
                    });
                    </script> 
                </div>
            </div>  
        <div id="Copyright">
            <hr />
            Copyright &copy: 2020 ROAMAR productions
        </div>
        </body>
</html>
