<html lang="en">

<head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" crossorigin="anonymous">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" crossorigin="anonymous">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" crossorigin="anonymous"></script>

</head>

<body>
    <div id="wrap">
        <div class="container">
            <div class="row">

                <form class="form-horizontal" action="/uploadCSV" method="post" name="upload_excel" enctype="multipart/form-data">
                    <fieldset>

                        <!-- Form Name -->
                        <center>
                            S<h2>Ilwin Joey Dcunha</h2><br>
                            <h2>1001390458</h2>
                            <img src=" {{url_for('static', filename='ilwin.jpg')}}" height="300" width="300" alt="No Image Available">
                        </center>
                        <br>
                        <br>

                        <!-- File Button -->
                        <div class="form-group">
                            <label class="col-md-4 control-label" for="filebutton">Select File</label>
                            <div class="col-md-4">
                                <input type="file" name="file" id="file1" class="input-large">
                            </div>
                        </div>

                        <!-- Button -->
                        <div class="form-group">
                            <label class="col-md-4 control-label" for="singlebutton">Import data</label>
                            <div class="col-md-4">
                                <button type="submit" id="submit" name="Import" class="btn btn-primary button-loading" data-loading-text="Loading...">Import</button>
                            </div>

                        </div>



                    </fieldset>
                </form>


                <form class="form-horizontal" action="/show" method="post" name="upload_image" enctype="multipart/form-data">
                    <fieldset>



                        <!-- File Button -->
                        <div class="form-group">
                            <label class="col-md-4 control-label" for="filebutton">Select Image</label>
                            <div class="col-md-4">
                                <input type="file" name="imageFile" id="file2" class="input-large">
                            </div>
                        </div>

                        <!-- Button -->
                        <div class="form-group">
                            <label class="col-md-4 control-label" for="singlebutton">upload image</label>
                            <div class="col-md-4">
                                <button type="submit" id="submit" name="sub" class="btn btn-primary button-loading" data-loading-text="Loading...">Upload</button>
                            </div>
                        </div>
                        <h2>File uploaded at path: {{ variable }}</h2>

                    </fieldset>
                </form>

                <a  href="/vehicle" >Click here for UI</img>

                 <a  href="/list" >Click here for Test</img>

            </div>
            <?php
               get_all_records();
            ?>
        </div>
    </div>
</body>

</html>