function AI() {
    this.solve = function(nextBoard) {
        alert(nextBoard);
        $.ajax({
          url: "demo.txt",
          async: false,
          cache: false
        }).done(function(data) {
            alert(data);
        });
        return [0, 0, 1, 1];
    }
}
