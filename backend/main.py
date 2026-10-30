job_export = job_df[
    ["job_title", "job_description", "clean_job"]
].copy()

# Preserve every row to maintain embedding alignment.
job_export["job_title"] = job_export["job_title"].fillna("")
job_export["job_description"] = job_export["job_description"].fillna("")
job_export["clean_job"] = job_export["clean_job"].fillna("")

assert len(job_export) == len(job_embeddings)

job_export.to_csv(
    os.path.join(ARTIFACT_DIR, "jobs_processed.csv"),
    index=False
)

print("Jobs:", len(job_export))
print("Embedding rows:", len(job_embeddings))