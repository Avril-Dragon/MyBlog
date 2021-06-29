function getQueryVariable(variable)
{
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        if(pair[0] == variable){return pair[1];}
    }
    return(false);
}
function Shadow(){
    var myURL = getQueryVariable("view");
    if(myURL=="timestamp")
    {
        //alert(myURL);
        document.getElementById("select").className="active";
    }
    if(myURL=="count")
    {
        //alert(myURL);
        document.getElementById("select2").className="active";
    }
    if(myURL=="reply")
    {
        //alert(myURL);
        document.getElementById("select3").className="active";
    }
}