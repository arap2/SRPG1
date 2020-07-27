<!DOCTYPE html>
<html>
    <head>
        <title>SARS-CoV-2 PDB Database</title>
        <link rel="stylesheet" type="text/css" href="PDB_DB.css" />
    </head>
    <body>
        <div id="Container">
            <!--Universal Navigation bar with class "selected" on the appropriate line-->
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
                            <a href="DNA_Table.php">DNA Database</a>
                            <a class="selected" href="PDB_table.php">PDB Database</a>
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
                <h1>SARS-CoV-2 PDB Database</h1>
            </div>
            <div id="Sequence_List">
                <p>This is the section where the protein structures are grouped by different ORF strains in a SQL database.</p>
                <hr />
                <div id="Seq_count_button">
                    <h2>Sequence Counter<h2>
                    <input type="button" id="btnGetCount" value="Sequence count" onclick = "CountRows()" />
                </div>
                <hr />
                <div id="DNA_Seq_Title">
                    <h2>Find a PDB structure</h2> 
                </div>
                <div class="DNA_search">
                    <form class="example">
                    <label for="MyInput">Search database by Orf or Release date (Example: "ORF3" or "2020-05-27"):</label><br>
                        <input ID="myInput" type="text" placeholder="Search for structures..." name="search"> 
                    </form>
                    <br />
                    <br />
                </div>
                <hr />
                <!--HTML table to be populated by PHP-->
                <table id="PHP_table">
                    <tr class="header">
                        <th>Accession</th>
                        <th>Release date</th>
                        <th>Description</th>
                        <th>Comment</th>
                        <th>Orf</th>
                        <th>Experimental Method</th>
                        <th>Reference</th>
                    </tr>
                    <?php
                    /*Assigning MySQL login details as variables*/
                    $servername = "localhost";
                    $username = "lampuser";
                    $password = "changeme";
                    $dbName = "Covid_19";
                    
                    /*Connecting to MySQL server*/
                    $connection = mysqli_connect($servername,$username,$password,$dbName);
                    
                    $sql_showtable = "select * from PDB_structures;";
                    $results = mysqli_query($connection, $sql_showtable);
                    
                    $resultsCheck = mysqli_num_rows($results);

                    /*Running SQL search then populating HTML columns*/
                    if($resultsCheck>0){
                        while($row = mysqli_fetch_assoc($results)){
                            echo "<tr><td>". $row['Accession']."\n"."</td><td>" .$row['Release_date']."\n". "</td><td>" .$row['Description']."\n"."</td><td>" .$row['Comment']."\n"."</td><td>" .$row['Orf']."\n"."</td><td>" .$row['Experimental_Method']."\n"."</td><td>" .$row['Reference']."<br/>".  "</td></tr>";
                        }
                    }
                    ?>
                </table>
                <!--Row counting function-->
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
                            var message = "PDB Sequence Count: " + rowCount;
                            alert(message);
                        }
                    </script>
                </div>
                <p>&nbsp;</p>
                </div>
                <!--Table searching function-->
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