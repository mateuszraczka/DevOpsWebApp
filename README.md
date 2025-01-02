# Instrukcje uruchomienia aplikacji:

1. Wymagania wstępne
Aby uruchomić aplikację, upewnij się, że masz zainstalowane następujące narzędzia:

Zainstaluj:
- Git
- Docker

2. Utworzenie fork tego repozytorium

Kroki do wykonania fork repozytorium:
  1. Zaloguj się na GitHub:
  Otwórz GitHub i zaloguj się na swoje konto.

  2. Otwórz repozytorium, które chcesz skopiować:
  Przejdź do repozytorium, które chcesz skopiować. W tym przypadku repozytorium aplikacji webowej.

  3. Wykonaj fork:
  W prawym górnym rogu strony repozytorium znajdziesz przycisk "Fork". Kliknij go.
  GitHub poprosi Cię o wybranie konta, na którym ma zostać utworzony fork. Wybierz swoje konto.

  4. Forkowanie repozytorium:
  Po kliknięciu "Fork" repozytorium zostanie skopiowane do Twojego konta GitHub. Twój fork będzie dostępny pod adresem:
  https://github.com/<twoje-uzytkownik>/<nazwa-repozytorium>
  Zamień <twoje-uzytkownik> na swoją nazwę użytkownika GitHub, a <nazwa-repozytorium> na nazwę repozytorium.

3. Sciągniecie repozytorium na komputer
Otwórz terminal/command prompt na swoim komputerze.

Sklonuj repozytorium z GitHub na swoje urządzenie:

git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>

- Zamień <your-username> na swoją nazwę użytkownika GitHub.
- Zamień <repository-name> na nazwę swojego repozytorium.

4. Budowanie obrazu Docker
Upewnij się, że znajdujesz się w katalogu z plikiem Dockerfile (w głównym katalogu repozytorium).

Zbuduj obraz Docker, wykonując poniższe polecenie:

docker build -t flask-app:latest .

flask-app to nazwa obrazu Docker. Możesz użyć innej nazwy, jeśli chcesz.
Proces budowania obrazu może chwilę potrwać.

5. Uruchamianie aplikacji w kontenerze Docker
Po zbudowaniu obrazu, uruchom aplikację w kontenerze Docker:

docker run -d -p 5000:5000 flask-app:latest

-d oznacza uruchomienie kontenera w tle.
-p 5000:5000 mapuje port 5000 na lokalnym komputerze do portu 5000 w kontenerze (domyślny port Flask).
flask-app:latest to nazwa i tag obrazu Docker.

6. Dostęp do aplikacji przez przeglądarkę
Po uruchomieniu kontenera, aplikacja będzie dostępna pod adresem:

http://localhost:5000
Otwórz przeglądarkę i wejdź na ten adres, aby zobaczyć działającą aplikację webową.


# Opis działania procesu CI:

1. Repozytorium Git i kod źródłowy
Wszystko zaczyna się od repozytorium Git, które zawiera kod aplikacji. Repozytorium może zawierać pliki, takie jak:

Kod źródłowy aplikacji (np. pliki Pythona z aplikacją webową w Flask).
Plik Dockerfile – umożliwiający konteneryzację aplikacji.
Plik konfiguracyjny CI – np. .github/workflows/ci.yml dla GitHub Actions.

2. Konfiguracja workflow CI w GitHub Actions
Plik konfiguracyjny CI (ci.yml) zawiera wszystkie kroki, które są automatycznie wykonywane przez GitHub Actions po każdym pushu lub pull requeście do repozytorium. Workflow ten jest zapisywany w katalogu .github/workflows/ w repozytorium.

3. Uruchomienie procesu CI
Proces CI jest wyzwalany w następujących sytuacjach:

- Push do gałęzi głównej (main): Kiedy deweloper wysyła zmiany do głównej gałęzi, CI automatycznie rozpoczyna swoją pracę.
- Pull Request: Kiedy tworzony jest pull request (PR) z innej gałęzi (np. dev) do głównej gałęzi, proces CI jest uruchamiany w celu weryfikacji kodu przed jego połączeniem z główną gałęzią.

Krok 1: Sprawdzenie kodu z repozytorium
Na początku workflow CI GitHub Actions pobiera (czyli klonuje) aktualne repozytorium na maszynę roboczą (wirtualną maszynę w systemie Ubuntu).

- name: Checkout repository
  uses: actions/checkout@v3
Checkout oznacza pobranie najnowszego kodu z repozytorium GitHub, aby workflow mógł działać na aktualnej wersji projektu.

Krok 2: Konfiguracja środowiska programistycznego
Jeśli aplikacja jest napisana w jakimś języku programowania (np. Python), CI musi przygotować odpowiednie środowisko.

- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.9'
W przypadku Pythona, GitHub Actions ustawia wersję Pythona, która ma być używana w projekcie.

Krok 3: Instalacja zależności
Kolejnym krokiem jest instalacja zależności, takich jak biblioteki zdefiniowane w pliku requirements.txt w przypadku Pythona.

- name: Install dependencies
  run: |
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
Tworzony jest wirtualny environment (venv), aktywowany, a następnie instalowane są wszystkie zależności z pliku requirements.txt.

Krok 4: Wykonanie testów
W tym kroku uruchamiane są testy aplikacji. W rzeczywistości, w tym miejscu można uruchomić wszystkie testy jednostkowe, ale w przypadku tego projektu testy mogą być symboliczne (np. polecenie echo "Test").

- name: Run Tests
  run: |
    echo "Run tests"
Jest to krok symulujący wykonanie testów aplikacji, który w przyszłości może być rozszerzony o rzeczywiste testy aplikacji, takie jak np. pytest.

Krok 5: Budowanie obrazu Docker
CI może również zawierać krok budowania obrazu Docker, w przypadku konteneryzacji aplikacji.

- name: Build Docker image
  run: docker build -t flask-app:latest .
Zawiera to komendę Docker docker build, która buduje obraz na podstawie pliku Dockerfile.

Krok 6: Logowanie do GitHub Container Registry
Jeśli proces CI ma również za zadanie wysłać zbudowany obraz Docker do GitHub Container Registry (GHCR), następuje etap logowania się do rejestru kontenerów.

- name: Log in to GitHub Container Registry
  uses: docker/login-action@v2
  with:
    registry: ghcr.io
    username: ${{ github.repository_owner }}
    password: ${{ secrets.DOCKER_SECRET }}
Za pomocą wtyczki docker/login-action CI loguje się do GitHub Container Registry z użyciem tokenu przechowywanego w secrets.DOCKER_SECRET.

Krok 7: Tagowanie obrazu Docker

Po zbudowaniu obrazu, przypisuje się mu odpowiednią nazwę i tag, aby mógł być wypchnięty do GitHub Container Registry.

- name: Tag Docker image
  run: |
    docker tag flask-app:latest ghcr.io/${{ github.repository_owner }}/devopswebapp:latest
W tym kroku obraz jest tagowany zgodnie z wymaganiami GHCR.

Krok 8: Push obrazu Docker do GitHub Container Registry
Na koniec, obraz jest wysyłany do GitHub Container Registry (GHCR), aby był dostępny do użycia w innych środowiskach lub przez innych deweloperów.

- name: Push Docker image to GitHub Container Registry
  run: |
    docker push ghcr.io/${{ github.repository_owner }}/devopswebapp:latest
Komenda docker push wysyła obraz na GitHub Container Registry, używając tagu przypisanego w poprzednim kroku.

4. Monitoring i raportowanie
Po zakończeniu procesu CI, GitHub Actions generuje raport, który można śledzić na stronie repozytorium w zakładce Actions. Raport ten pokazuje szczegółowe informacje na temat wykonania każdego kroku, w tym:

Czas wykonania poszczególnych etapów.
Wyniki testów (jeśli zostały wykonane).
Błędy i logi z poszczególnych kroków (np. błędy kompilacji, testów, czy budowania obrazu).

5. Zakończenie procesu CI
Po zakończeniu procesu CI, kod zostaje zweryfikowany, a obraz Docker wypchnięty do rejestru, jeśli proces zakończył się pomyślnie. Jeśli wystąpił jakiś błąd (np. testy nie przeszły, błąd w Dockerze), proces CI zakończy się niepowodzeniem, a deweloper otrzyma odpowiednie powiadomienie.
