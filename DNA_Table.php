<!DOCTYPE html>
<html>
    <head>
        <!--Head section displays the title and links the CSS style page for page formatting-->
        <title>SARS-CoV-2 DNA Database</title>
        <link rel="stylesheet" type="text/css" href="DNA_DB.css" />
    </head>
    <body>
        <!--Container is everything on the actual page, used for universal CSS commands-->
        <div id="Container">
            <!--Universal layout of every navigation bar at the top of every page-->
            <div id="Navigation">
                <a href="index.html">Title</a>
                <a href="home_page.html">Home</a>
                <a href="History_page.html">History</a>
                    <div class="dropdown">
                        <button class="dropbutton">Genetic Databases
                            <i class="fa fa-caret-down"></i>
                        </button>
                        <div class="dropdown_content">
                            <a href="Pro_table.php">Protein Database</a>
                            <a class="selected" href="DNA_Table.php">DNA Database</a>
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
                <h1>SARS-CoV-2 DNA Database</h1>
            </div>
            <!--Contents of the page-->
            <div id="Sequence_List">
                <p>This is the section where the DNA sequences are grouped by different ORF strains in a SQL database.</p>
                <hr />
                <div id="Seq_count_button">
                    <h2>Sequence Counter<h2>
                    <input type="button" id="btnGetCount" value="Sequence count" onclick = "CountRows()" />
                </div>
                <hr />
                <div id="DNA_Seq_Title">
                    <h2>Find a DNA Sequence</h2> 
                </div>
                <div class="DNA_search">
                    <form class="example">
                    <label for="MyInput">Search database by Release date or Accesion number (Example: "2020-02-29" or "LC528232.1_E "):</label><br>
                        <input ID="myInput" type="text" placeholder="Search for sequences..." name="search"> 
                    </form>
                    <br />
                    <br />
                </div>
                <hr />
                <!--PHP connects MySQL table and displays in HTML table-->
                <table id="PHP_table">
                    <tr class="header">
                        <th>Accession</th>
                        <th>ORF Coordinates</th>
                        <th>ORF Product</th>
                        <th>FASTA sequence</th>
                        <th>Release Date</th>
                        <th>Reference</th>
                    </tr>
                    <?php
                    /*Assigning login details as variables, easier to use*/
                    $servername = "localhost";
                    $username = "lampuser";
                    $password = "changeme";
                    $dbName = "Covid_19";
                    
                    /*Connection to MySQL using login variables*/
                    $connection = mysqli_connect($servername,$username,$password,$dbName);
                    
                    /*Run SQL query to select all from covid_nucleotide table*/
                    $sql_showtable = "select * from covid_nucleotide;";
                    $results = mysqli_query($connection, $sql_showtable);
                    
                    $resultsCheck = mysqli_num_rows($results);
                    /*If/While to run through every row of the MySQL table and populate the HTML table*/
                    if($resultsCheck>0){
                        while($row = mysqli_fetch_assoc($results)){
                            echo "<tr><td>". $row['ACCESSION']."\n". "</td><td>" .$row['ORF_COORDINATES']."\n"."</td><td>" .$row['ORF_PRODUCT']."\n"."</td><td>" .$row['FASTA']."\n"."</td><td>" .$row['RELEASE_DATE']."\n"."</td><td>" .$row['REFERENCE']. "<br/>". "</td></tr>";
                        }
                    }
                    ?>
                </table>
                </div>
                <!--Counter looks at number of rows in HTML table to give sequence count-->
                <div id="Table_length_count">
                    <script type="text/javascript">
                        function CountRows() {
                            /*Set counting variables as zero*/
                            var totalRowCount = 0;
                            var rowCount = 0;
                            var table = document.getElementById("PHP_table");
                            var rows = table.getElementsByTagName("tr")
                            /*For/If loop to run through every row of the HTML table*/
                            for (var i = 0; i < rows.length; i++) {
                                totalRowCount++;
                                if (rows[i].getElementsByTagName("td").length > 0) {
                                    rowCount++;
                                }
                            }
                            var message = "DNA Sequence Count: " + rowCount;
                            alert(message);
                        }
                    </script>
                </div>
                <!--Searches HTML table to find best possible matches-->
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
