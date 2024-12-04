# Mock Data Generation for Healthcare

## Current Mock Data for the Benchmark
Feel free to use some of the data for other purposes.
- `users.json`: a database of patients with their emails, dates of birth (DOB), contact information, and primary care providers (PCP).
- `appointments.json`: a database of scheduled appointments, including appointment type (e.g., consultation, check-up), provider information, and status (e.g., scheduled, completed, canceled).
- `insurance.json`: a database of insurance policies, including policy numbers, coverage types, deductible limits, and co-pays.

Check `../tools` for mock APIs on top of the current mock data.

### Experience of Mock Data Generation

Read our paper to learn more about the generation process for each database. In general, it involves the following stages:

1. **Design the type and schema of each database**  
   - This step defines the structure and relationships between patient records, appointments, and insurance details. You can use GPT for brainstorming schema ideas, but all final decisions should be made by humans since they serve as the foundation for downstream tasks.

2. **Identify programmatically generated vs. GPT-generated components**  
   - Determine which elements of the schema require creative generation (e.g., patient names, cities) versus those that can be reliably generated through programming (e.g., policy numbers, appointment statuses). Examples:
     - Patient names (e.g., Sara, John, Noah) and healthcare provider specialties (e.g., cardiology, pediatrics) need GPT generation.
     - Appointment times and insurance co-pay amounts can be programmatically generated.

3. **Generate seed data using GPT and augment with programmatic methods**  
   - Use GPT to generate initial seed data, such as first names, last names, or common medical conditions. Combine this with programmatic data to create comprehensive datasets. For example:
     - Generate a list of patient profiles with GPT (name, DOB, city).
     - Use code to assign programmatically generated attributes like policy numbers, appointment times, or coverage tiers.
   - GPT can assist in writing the code for data generation but should not replace programmatic database construction to ensure diversity and reliability.

This approach ensures a balance between creativity and structured data generation, enabling accurate and scalable mock healthcare datasets.