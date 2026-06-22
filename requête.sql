-- Connexion à la base, ont sélectionne tout de la base Kalicea.ligne_bon_vente
select * from kalicea.ligne_bon_vente

-- Commande pour filtrer le tableau rapidement selon une condition
where "nom de colone" = "entrer valeur ou  une condition"

-- Commande pour rajouter des condition plus spécifiques après un premier filtrages
and 'nom colone' in "entrer valeur ou une condition"

-- A mettre à la suite d'un where ou d'un and pour re rajouter une autre condition
or 

-- Permet de trier les résultats
order by 

-- Permet d'agréger les lignes
group by