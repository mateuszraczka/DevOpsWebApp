# Instrukcja Uruchomienia Aplikacji

## Wymagania wstępne

Aby uruchomić aplikację, upewnij się, że masz zainstalowane następujące narzędzia:

- **Git**
- **Docker**

## Utworzenie Fork Repozytorium

Aby rozpocząć, wykonaj fork repozytorium, aby skopiować aplikację na swoje konto GitHub.

### Kroki do wykonania fork repozytorium:

1. **Zaloguj się na GitHub**: Otwórz GitHub i zaloguj się na swoje konto.
2. **Otwórz repozytorium, które chcesz skopiować**: Przejdź do repozytorium, które chcesz skopiować. W tym przypadku repozytorium aplikacji webowej.
3. **Wykonaj fork**: W prawym górnym rogu strony repozytorium znajdziesz przycisk "Fork". Kliknij go. GitHub poprosi Cię o wybranie konta, na którym ma zostać utworzony fork. Wybierz swoje konto.
4. **Forkowanie repozytorium**: Po kliknięciu "Fork" repozytorium zostanie skopiowane do Twojego konta GitHub. Twój fork będzie dostępny pod adresem: `https://github.com/USERNAME/REPOSITORY_NAME`. Zamień `USERNAME` na swoją nazwę użytkownika GitHub, a `REPOSITORY_NAME` na nazwę repozytorium.

## Ściągnięcie Repozytorium na Komputer

Otwórz terminal/command prompt na swoim komputerze.

Sklonuj repozytorium z GitHub na swoje urządzenie:

```bask
git clone https://github.com/USERNAME/REPOSITORY_NAME.git
cd REPOSITORY_NAME
```
Zamień USERNAME na swoją nazwę użytkownika GitHub. Zamień REPOSITORY_NAME na nazwę swojego repozytorium.

## Budowanie Obrazu Docker
Upewnij się, że znajdujesz się w katalogu z plikiem Dockerfile (w głównym katalogu repozytorium). Zbuduj obraz Docker, wykonując poniższe polecenie:

```bash
docker build -t flask-app:latest .
```
flask-app to nazwa obrazu Docker. Możesz użyć innej nazwy, jeśli chcesz. Proces budowania obrazu może chwilę potrwać.

## Uruchamianie Aplikacji w Kontenerze Docker
Po zbudowaniu obrazu, uruchom aplikację w kontenerze Docker:

```bash
docker run -d -p 5000:5000 flask-app:latest
```
-d oznacza uruchomienie kontenera w tle.
-p 5000:5000 mapuje port 5000 na lokalnym komputerze do portu 5000 w kontenerze (domyślny port Flask).
flask-app:latest to nazwa i tag obrazu Docker.

## Dostęp do Aplikacji przez Przeglądarkę
Po uruchomieniu kontenera, aplikacja będzie dostępna pod adresem:

**http://localhost:5000**

Otwórz przeglądarkę i wejdź na ten adres, aby zobaczyć działającą aplikację webową.

# Opis Działania Procesu CI
## Repozytorium Git i Kod Źródłowy
Wszystko zaczyna się od repozytorium Git, które zawiera kod aplikacji. Repozytorium może zawierać pliki, takie jak:

Kod źródłowy aplikacji (np. pliki Pythona z aplikacją webową w Flask).
Plik Dockerfile – umożliwiający konteneryzację aplikacji.
Plik konfiguracyjny CI – np. .github/workflows/ci.yml dla GitHub Actions.

## Konfiguracja Workflow CI w GitHub Actions
Plik konfiguracyjny CI (ci.yml) zawiera wszystkie kroki, które są automatycznie wykonywane przez GitHub Actions po każdym pushu lub pull requeście do repozytorium. Workflow ten jest zapisywany w katalogu .github/workflows/ w repozytorium.

## Uruchomienie Procesu CI
Proces CI jest wyzwalany w następujących sytuacjach:

- Push do gałęzi głównej (main): Kiedy deweloper wysyła zmiany do głównej gałęzi, CI automatycznie rozpoczyna swoją pracę.
- Pull Request: Kiedy tworzony jest pull request (PR) z innej gałęzi (np. dev) do głównej gałęzi, proces CI jest uruchamiany w celu weryfikacji kodu przed jego połączeniem z główną gałęzią.

### Krok 1: Sprawdzenie Kodu z Repozytorium
Na początku workflow CI GitHub Actions pobiera (czyli klonuje) aktualne repozytorium na maszynę roboczą (wirtualną maszynę w systemie Ubuntu).

```yaml
name: Checkout repository
uses: actions/checkout@v3
```
Checkout oznacza pobranie najnowszego kodu z repozytorium GitHub, aby workflow mógł działać na aktualnej wersji projektu.
Krok 2: Konfiguracja Środowiska Programistycznego
Jeśli aplikacja jest napisana w jakimś języku programowania (np. Python), CI musi przygotować odpowiednie środowisko.

```yaml
name: Set up Python
uses: actions/setup-python@v4
with:
  python-version: '3.9'
```
W przypadku Pythona, GitHub Actions ustawia wersję Pythona, która ma być używana w projekcie.

### Instalacja Zależności
Kolejnym krokiem jest instalacja zależności, takich jak biblioteki zdefiniowane w pliku requirements.txt w przypadku Pythona.

```yaml
name: Install dependencies
run: |
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```
Tworzony jest wirtualny environment (venv), aktywowany, a następnie instalowane są wszystkie zależności z pliku requirements.txt.

### Wykonanie Testów
W tym kroku uruchamiane są testy aplikacji. W rzeczywistości, w tym miejscu można uruchomić wszystkie testy jednostkowe, ale w przypadku tego projektu testy mogą być symboliczne (np. polecenie echo "Test").

```yaml
name: Run Tests
run: |
  echo "Run tests"
```
Jest to krok symulujący wykonanie testów aplikacji, który w przyszłości może być rozszerzony o rzeczywiste testy aplikacji, takie jak np. pytest.

### Budowanie Obrazu Docker
CI może również zawierać krok budowania obrazu Docker, w przypadku konteneryzacji aplikacji.

```yaml
name: Build Docker image
run: docker build -t flask-app:latest .
```
Zawiera to komendę Docker docker build, która buduje obraz na podstawie pliku Dockerfile.

### Logowanie do GitHub Container Registry
Jeśli proces CI ma również za zadanie wysłać zbudowany obraz Docker do GitHub Container Registry (GHCR), następuje etap logowania się do rejestru kontenerów.

```yaml
name: Log in to GitHub Container Registry
uses: docker/login-action@v2
with:
  registry: ghcr.io
  username: ${{ github.repository_owner }}
  password: ${{ secrets.DOCKER_SECRET }}
```
Za pomocą wtyczki docker/login-action CI loguje się do GitHub Container Registry z użyciem tokenu przechowywanego w secrets.DOCKER_SECRET.

### Tagowanie Obrazu Docker
Po zbudowaniu obrazu, przypisuje się mu odpowiednią nazwę i tag, aby mógł być wypchnięty do GitHub Container Registry.

```yaml
name: Tag Docker image
run: |
  docker tag flask-app:latest ghcr.io/${{ github.repository_owner }}/devopswebapp:latest
```
W tym kroku obraz jest tagowany zgodnie z wymaganiami GHCR.

### Push Obrazu Docker do GitHub Container Registry
Na koniec, obraz jest wysyłany do GitHub Container Registry (GHCR), aby był dostępny do użycia w innych środowiskach lub przez innych deweloperów.

```yaml
name: Push Docker image to GitHub Container Registry
run: |
  docker push ghcr.io/${{ github.repository_owner }}/devopswebapp:latest
```

Komenda docker push wysyła obraz na GitHub Container Registry, używając tagu przypisanego w poprzednim kroku.

## Monitoring i Raportowanie
Po zakończeniu procesu CI, GitHub Actions generuje raport, który można śledzić na stronie repozytorium w zakładce Actions. Raport ten pokazuje szczegółowe informacje na temat wykonania każdego kroku, w tym:

Czas wykonania poszczególnych etapów.
Wyniki testów (jeśli zostały wykonane).
Błędy i logi z poszczególnych kroków (np. błędy kompilacji, testów, czy budowania obrazu).

## Zakończenie Procesu CI
Po zakończeniu procesu CI, kod zostaje zweryfikowany, a obraz Docker wypchnięty do rejestru, jeśli proces zakończył się pomyślnie. Jeśli wystąpił jakiś błąd (np. testy nie przeszły, błąd w Dockerze), proces CI zakończy się niepowodzeniem, a deweloper otrzyma odpowiednie powiadomienie.
