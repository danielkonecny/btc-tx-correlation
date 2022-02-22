# Zadání

K dispozici dostanete dataset obsahující informace o potenciálně uskutečněných prodejích produktů na některých vybraných temných tržištích (darknet marketplace). Tento dataset obsahuje následující informace:

* datum a čas zaznamenání prodeje
* relevantní informace o prodaném produktu a službách
	* možné ceny dopravy
	* možné množstevní varianty a odpovídající ceny

Vašim cílem bude implementace nástroje pro korelaci existujících transakcí v Bitcoin blockchainu s daty z výše zmíněného datasetu. K implementaci můžete využít libovolný programovací jazyk a jakékoliv relevantní nástroje a knihovny třetích stran. Součástí řešení projektu bude i dokumentace, kde bude popsáno:

* použité knihovny a nástroje,
* zvolené či navržené korelační metody,
* implementace výsledného nástroje,
* dosažené výsledky - benchmark, potenciální úspěšnost korelace atd.

V případě nejasností či dalších otázek k zadání kontaktujte zadávajícího projektu.

# Shrnutí

Hlavními cíli tohoto projektu je tedy:

1. zmapování či návrh korelačních metod pro Bitcoin transakce v závislosti na poskytnutém datasetu,
2. analýza a implementace vybraných metod v rámci automatizovaného korelačního nástroje pro libovolný subset Bitcoin transakcí,
3. zhodnocení dosažených výsledků.

# Databáze

Na [NextCloudu](https://nextcloud.fit.vutbr.cz/s/aLwnTJiLPEYpDaF) najdete dataset, který budete pro účely tohoto projektu potřebovat. Archiv (2.3 GB) obsahuje SQL skripty pro vytvoření tabulek a CSV soubory s daty (po extrakci přibližně 10GB), které budete do cílových tabulek (ve vaší lokální PostgreSQL databázi) moci jednoduše importovat pomocí:

`psql -d "$DATABASE_NAME" -c "\COPY $TABLE_NAME FROM $TABLE_NAME.csv CSV"`

Funkcionalita s PostgreSQL a danými tabulkovými strukturami je vyžadována. Případné optimalizace v daných schématech jsou po konzultaci a schválení možné.
