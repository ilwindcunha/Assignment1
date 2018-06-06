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

                <form class="form-horizontal" action="/search" method="post" name="upload_excel" >
                   <lable>Course Number </lable> <input type="text" name="courceNo">
                   <lable>Course day </lable> <input type="text" name="day">

                   <button type="submit" id="submit" name="Import" class="btn btn-primary button-loading" data-loading-text="Loading...">Submit</button>
                </form>
            </div>
            <?php
               get_all_records();
            ?>
        </div>
    </div>
</body>

</html>