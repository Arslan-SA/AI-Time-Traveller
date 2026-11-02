# Contributing to AI Time Traveler

Thanks for your interest in improving AI Time Traveler. Contributions, ideas, and feedback are welcome.

## Contribution workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

Please open an issue first for major changes so we can discuss direction.

## Good first areas

- Forecasting model evaluation
- Uncertainty visualization
- New data-source connectors
- Test coverage
- Documentation

## Development setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Code style

Install the Git hooks once per clone:

```bash
pip install pre-commit
pre-commit install
```

The hooks run Ruff and Black on backend Python files and Prettier on frontend files. To run every hook against the whole repository:

```bash
pre-commit run --all-files
```
