from controller import run_pipeline
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python app/main.py <persona> <job-to-be-done>")
        sys.exit(1)

    persona = sys.argv[1]
    job = sys.argv[2]

    if not persona.strip():
        print("Error: Persona cannot be empty")
        sys.exit(1)

    if not job.strip():
        print("Error: Job-to-be-done cannot be empty")
        sys.exit(1)

    print(f"Starting PDF extraction for persona: {persona}\nJob to be done: {job}\n{'-'*50}")

    try:
        run_pipeline(persona, job)
        print("\n✅ Extraction completed successfully!")
        print("📄 Check output/results.json for results")
    except Exception as e:
        print(f"\n❌ Error during extraction: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
