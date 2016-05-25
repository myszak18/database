<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Search by Gene</title>
 
    
    <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
 
    <link href="http://getbootstrap.com/examples/jumbotron-narrow/jumbotron-narrow.css" rel="stylesheet">
	<link href="../static/signup.css" rel="stylesheet">
    <script src="../static/js/jquery-2.2.3.min.js"></script>
    <script>
    function showHint(str) {
    if (str.length == 0) { 
        document.getElementById("txtHint").innerHTML = "";
        return;
    } else {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                document.getElementById("txtHint").innerHTML = xmlhttp.responseText;
            }
        };
        xmlhttp.open("GET", "../static/gethint.php?q=" + str, true);
        xmlhttp.send();
    }
}
</script>
  </head>
 
  <body>
 
    <div class="container">
      <div class="header">
        <nav>
          <ul class="nav nav-pills pull-right">
            <li role="presentation" ><a href="/">Home</a></li>
            <li role="presentation" class="active"><a href="#">Search Gene</a></li>
            <li role="presentation" ><a href="/showSignUp">Sign Up</a></li>
          </ul>
        </nav>
        <h3 class="text-muted">Polish Exome Database</h3>
      </div>
 
      <div class="jumbotron">
        <h1>Polish Exome Database</h1>
        <form class="form-signin" action="/validateGene" method="post" >
        <label for="inputEmail" class="sr-only">Gene</label>
        <input type="text" name="gene" id="gene" class="form-control" placeholder="HGNC gene symbol" required autofocus onkeyup="showHint(this.value)">
        <button id="btnSearch" class="btn btn-lg btn-primary btn-block" type="submit">Search Gene</button>
      </form>
      <p>Suggestions: <span id="txtHint"></span></p>
      </div>
 
       
 
      <footer class="footer">
        <p>&copy; Company 2015</p>
      </footer>
 
    </div>
  </body>
</html>
