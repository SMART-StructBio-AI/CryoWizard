
# Use CryoWizard via Chrome Extension


## Regenerate extension.zip

Typically, the `extension.zip` file is automatically generated in the `/path/to/CryoWizard` directory during the installation process. If you accidentally delete it, you also can manually regenerate the file by running:

    (cryowizard) $ cd path/to/CryoWizard
    (cryowizard) $ python CryoWizard.py --GenerateExtensionPackege


## CryoWizard job inputs & parameters
   
### Inputs

- **cryowizard pipeline default**: Supported inputs: Movie, Micrograph, or Particle. Supports single, multiple, or mixed-type inputs concurrently.
- **cryowizard pipeline simpler**: Supported inputs: Movie, Micrograph, or Particle. Supports single, multiple, or mixed-type inputs concurrently.
- **cryoranker only**: Supported inputs: Movie, Micrograph, or Particle. Supports single, multiple, or mixed-type inputs concurrently.
- **cryoranker get top particles**: Supported inputs: CryoRanker job. Supports single or multiple inputs.
- **custom**: None


### Parameters

- **CryoWizard pipeline type**: pipeline types, selecting different pipeline types will require different parameters.
   - **cryowizard pipeline default**: Standard pipeline. It begins with an initial round of particle picking using a Blob Picker, followed by CryoRanker and a few rounds of NU-Refinement to generate a 3D volume. Subsequently, if the input includes movies or micrographs, the pipeline will automatically perform Template Picking on them using the initial 3D volume. All resulting particles then undergo another round of CryoRanker and NU-Refinement to produce a new 3D volume, followed by post-processing for the final result.
   - **cryowizard pipeline simpler**: A streamlined version that only performs a single round of particle picking using the Blob Picker, followed by CryoRanker, NU-Refinement, and post-processing to obtain the final 3D volume.
   - **cryoranker only**: The pipeline only executes pre-processing and CryoRanker, skipping all subsequent refinement steps.
   - **cryoranker get top particles**: Requires an existing CryoRanker job as input. This mode filters particles based on CryoRanker scores, allowing you to select particles above a specific threshold or extract a fixed number of high-quality particles sorted by score.
   - **custom**: A non-preset mode that performs no automated actions.
- **Pixel Size (A)**: Pixel size of inputs data.
- **Average Particle diameter (A)**: Average diameters of target molecular  (usually protein)
- **CTF fit resolution**: Filter micrographs by CTF resolution. Example: `0,6` retains only those within the 0–6 A range.
- **Symmetry**: Protein symmetry.
- **Number of GPUs for Multi-GPU CryoSPARC jobs**: Number of GPUs for Multi-GPU CryoSPARC jobs.
- **Inference GPU ids**: During pipeline execution, if model inference (e.g., CryoRanker) is running locally rather than being submitted via Slurm, you can use this parameter to specify which GPUs to use. For example, entering `0,1` will allocate GPU 0 and GPU 1.
- **Get type**: Particle selection mode for "cryoranker get top particles":
   - **Number**: Selects a specific number of high-quality particles.
   - **Score**: Selects particles with a score above a specified threshold. (Scores range from 0 to 1, where 1 represents the highest quality).
- **Particle cut-off point**: Particle selection cut-off point, relative to `Get type` parameter
   

