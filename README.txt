

I) Subir contenido al servidor

II) Uso de github

echo "# PuntoDeVentaWeb" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin git@github.com:sazpeitia/PuntoDeVentaWeb.git
git push -u origin master
