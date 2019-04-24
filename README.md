# Manifest Data Element

### What are manifest files: 
NDA has added a new Data Element of type Manifest to the existing set of String, Integer, Float, Thumbnail, File, and GUID. This effort was done primarily to support the BIDS format for imaging data. The Manifest data element is like the File data element in that the data submission template specifies the location of an XML or JSON file containing a collection of files. This supports the capability to create NDA data structures that describe a collection of related file resources. For example, this could be the output from a neuroimaging analysis pipeline. A Manifest file will consist of four required fields: path, name, size, and md5sum for each file listed. 

### What are manifests used for:
Previously those who wanted to share this kind of data would have to create an archive (.zip, .tar) of the output and submit the archive using a File data element type. This new element treats the files included in the Manifest as associated files for purposes of submission and these are ingested and stored as individual objects in AWS S3 Object storage, which also enables users to directly access specific files from the collection of files without having to download and unpack the entire archive. 

#### Examples:
Below is a directory tree for data of a single subject:

```bash
/Users/Downloads/ManifestTestData1/Documentation/100206

├── T1w

│   ├── Diffusion

│   │   ├── bvals

│   │   ├── bvecs

│   │   ├── data.nii.gz

│   │   ├── eddylogs

│   │   │   ├── eddy_unwarped_images.eddy_movement_rms

│   │   │   ├── eddy_unwarped_images.eddy_outlier_map

│   │   │   ├── eddy_unwarped_images.eddy_outlier_n_sqr_stdev_map

│   │   │   ├── eddy_unwarped_images.eddy_outlier_n_stdev_map

│   │   │   ├── eddy_unwarped_images.eddy_outlier_report

│   │   │   ├── eddy_unwarped_images.eddy_parameters

│   │   │   ├── eddy_unwarped_images.eddy_post_eddy_shell_alignment_parameters

│   │   │   └── eddy_unwarped_images.eddy_restricted_movement_rms

│   │   ├── grad_dev.nii.gz

│   │   └── nodif_brain_mask.nii.gz

│   └── T1w_acpc_dc_restore_1.25.nii.gz

└── release-notes

    └── ReleaseNotes.txt
```

Previously, to submit this in an image03 data structure, the directory would have to be zipped up and submitted as a single archived file, as seen below. If a user wanted to access the data in the archive, they would have to download and unzip the entire file to extract a single image. 


| image | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|------------------|------------------|----------------|---------------|-----|---------------------|------------------------------------------|----------------------|-------------------|-------------------|----------------|-------------------------|-----------------|------------------------------|-------------------------|------------------------|------------|--------------------|----------------------|------------------|--------------------|--------------|---------------|--------------------------|---------------------|---------------|----------------------|---------------|---------------|---------------|---------------|--------------|---------------|--------------|-------------|-------------|-------------|-------------|-------------|-------------------|-------------------|-------------------|-------------------|-------------------|-----------------------|-------------------|------------|----------------|----------------------|-------------|------------|------------------|---------------------------|-----------------|------------------|----------------|------------|-----------------|-----------|-------------------|------------------|-----------|---------------|-------------|-----------------|-------------------|-------|------|------------------------|-----------------------|--------------|----------|----------|-----------------|--------------------|----------|--------|------------------|
| SUBJECTKEY | SRC_SUBJECT_ID | INTERVIEW_DATE | INTERVIEW_AGE | SEX | COMMENTS_MISC | IMAGE_FILE | IMAGE_THUMBNAIL_FILE | IMAGE_DESCRIPTION | IMAGE_FILE_FORMAT | IMAGE_MODALITY | SCANNER_MANUFACTURER_PD | SCANNER_TYPE_PD | SCANNER_SOFTWARE_VERSIONS_PD | MAGNETIC_FIELD_STRENGTH | MRI_REPETITION_TIME_PD | FLIP_ANGLE | ACQUISITION_MATRIX | MRI_FIELD_OF_VIEW_PD | PATIENT_POSITION | PHOTOMET_INTERPRET | RECEIVE_COIL | TRANSMIT_COIL | TRANSFORMATION_PERFORMED | TRANSFORMATION_TYPE | IMAGE_HISTORY | IMAGE_NUM_DIMENSIONS | IMAGE_EXTENT1 | IMAGE_EXTENT2 | IMAGE_EXTENT3 | IMAGE_EXTENT4 | EXTENT4_TYPE | IMAGE_EXTENT5 | EXTENT5_TYPE | IMAGE_UNIT1 | IMAGE_UNIT2 | IMAGE_UNIT3 | IMAGE_UNIT4 | IMAGE_UNIT5 | IMAGE_RESOLUTION1 | IMAGE_RESOLUTION2 | IMAGE_RESOLUTION3 | IMAGE_RESOLUTION4 | IMAGE_RESOLUTION5 | IMAGE_SLICE_THICKNESS | IMAGE_ORIENTATION | QC_OUTCOME | QC_DESCRIPTION | QC_FAIL_QUEST_REASON | PET_ISOTOPE | PET_TRACER | DECAY_CORRECTION | TIME_DIFF_INJECT_TO_IMAGE | TIME_DIFF_UNITS | FRAME_START_UNIT | FRAME_END_UNIT | DATA_FILE2 | DATA_FILE2_TYPE | SCAN_TYPE | SLICE_ACQUISITION | SOFTWARE_PREPROC | PULSE_SEQ | EXPERIMENT_ID | SCAN_OBJECT | FRAME_END_TIMES | FRAME_START_TIMES | STUDY | WEEK | EXPERIMENT_DESCRIPTION | VISIT | SLICE_TIMING | BVECFILE | BVALFILE | BVEK_BVAL_FILES | DEVICESERIALNUMBER | PROCDATE | VISNUM | MRI_ECHO_TIME_PD |
| NDAR_INV25KAJM0U | NDAR_INV25KAJM0U | 6/4/17 | 109 | M | MB2 fMRI Fieldmap P | 100206_3T_Diffusion_preproc_manifest.tgz |  | ABCD-fMRI-FM-PA | fMRI | MRI | Philips Medical Systems | Achieva dStream | ["5.3.0", "5.3.0.0"] | 3 | 7 | 52 | [92, 0, 0, 89] |  | HFS | MONOCHROME2 | MULTI COIL |  | No |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 |  |  |  |  | 2.4 |  |  |  | NA |  |  |  |  |  |  |  |  |  | Field Map |  |  |  |  | Live |  |  |  |  |  | baseline_year_1_arm_1 |  |  |  |  | anonb2d4 |  |  | 0.07 |



With the addition of a Manifest data element, users can submit a Manifest file in JSON or XML format instead of an archive. The JSON Manifest file for this data would look like:



```javascript
{"files": [
{"path": "100206/T1w/Diffusion/data.nii.gz", "name": "data.nii.gz", "size": "1495985608", "md5sum": "fc9de773b7a010b3244b2ba41401081f"}, 
{"path": "100206/T1w/Diffusion/grad_dev.nii.gz", "name": "grad_dev.nii.gz", "size": "47617123", "md5sum": "cca9e024d5c15436a9603d699ea22597"}, 
{"path": "100206/T1w/Diffusion/nodif_brain_mask.nii.gz", "name": "nodif_brain_mask.nii.gz", "size": "68472", "md5sum": "0593dbde419cb4c44828dcac2adc6fde"}, 
{"path": "100206/T1w/Diffusion/bvecs", "name": "bvecs", "size": "9507", "md5sum": "46ec28bf7925e9643c047451ed5a1f44"},
{"path": "100206/T1w/Diffusion/bvals", "name": "bvals", "size": "1342", "md5sum": "a6a45f24b4e9cbe4ee23f49c2ded656c"},
{"path": "100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_outlier_n_sqr_stdev_map", "name": "eddy_unwarped_images.eddy_outlier_n_sqr_stdev_map", "size": "536486", "md5sum": "4c9d9ca400f1bd82e46f5346b6537f39"},
{"path": "100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_post_eddy_shell_alignment_parameters", "name": "eddy_unwarped_images.eddy_post_eddy_shell_alignment_parameters", "size": "2171", "md5sum": "456b19b6dcc37a74cf6652e5f79fc11c"}, 
{"path": "100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_outlier_report", "name": "eddy_unwarped_images.eddy_outlier_report", "size": "8216", "md5sum": "7e0db23168be7a3402e42565da1da6a4"}, 
{"path": "100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_outlier_map", "name": "eddy_unwarped_images.eddy_outlier_map", "size": "127363", "md5sum": "2fdc71a8257097b99b36e70757d641d3"}, 
{"path": "100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_movement_rms", "name": "eddy_unwarped_images.eddy_movement_rms", "size": "15838", "md5sum": "d779a75a17612c44a1c682310b5be888"}, 
{"path": "100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_parameters", "name": "eddy_unwarped_images.eddy_parameters", "size": "141660", "md5sum": "c8b5bd5e3a1e58cfe73e721ebf0a9632"}, 
{"path": "100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_restricted_movement_rms", "name": "eddy_unwarped_images.eddy_restricted_movement_rms", "size": "16085", "md5sum": "e18c13056e5af8b5be919ad318f35c3d"},
{"path": "100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_outlier_n_stdev_map", "name": "eddy_unwarped_images.eddy_outlier_n_stdev_map", "size": "536216", "md5sum": "8fdb960e863512050b108faada7a3c96"}, 
{"path": "100206/T1w/T1w_acpc_dc_restore_1.25.nii.gz", "name": "T1w_acpc_dc_restore_1.25.nii.gz", "size": "13256170", "md5sum": "f988fb4d12613ae903be1caed06d18b0"}, 
{"path": "100206/release-notes/ReleaseNotes.txt", "name": "ReleaseNotes.txt", "size": "786", "md5sum": "09d38e5ad2c4da76f6a2e048eda0032a"}]}

```

Alternatively, the XML file would look like:


```xml
<?xml version="1.0"?>
<manifestFile>
   <file>
      <md5sum>fc9de773b7a010b3244b2ba41401081f</md5sum>
      <name>data.nii.gz</name>
      <path>100206/T1w/Diffusion/data.nii.gz</path>
      <size>1495985608</size>
   </file>
   <file>
      <md5sum>cca9e024d5c15436a9603d699ea22597</md5sum>
      <name>grad_dev.nii.gz</name>
      <path>100206/T1w/Diffusion/grad_dev.nii.gz</path>
      <size>47617123</size>
   </file>
   <file>
      <md5sum>0593dbde419cb4c44828dcac2adc6fde</md5sum>
      <name>nodif_brain_mask.nii.gz</name>
      <path>100206/T1w/Diffusion/nodif_brain_mask.nii.gz</path>
      <size>68472</size>
   </file>
   <file>
      <md5sum>46ec28bf7925e9643c047451ed5a1f44</md5sum>
      <name>bvecs</name>
      <path>100206/T1w/Diffusion/bvecs</path>
      <size>9507</size>
   </file>
   <file>
      <md5sum>a6a45f24b4e9cbe4ee23f49c2ded656c</md5sum>
      <name>bvals</name>
      <path>100206/T1w/Diffusion/bvals</path>
      <size>1342</size>
   </file>
   <file>
      <md5sum>4c9d9ca400f1bd82e46f5346b6537f39</md5sum>
      <name>eddy_unwarped_images.eddy_outlier_n_sqr_stdev_map</name>
      <path>100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_outlier_n_sqr_stdev_map</path>
      <size>536486</size>
   </file>
   <file>
      <md5sum>456b19b6dcc37a74cf6652e5f79fc11c</md5sum>
      <name>eddy_unwarped_images.eddy_post_eddy_shell_alignment_parameters</name>
      <path>100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_post_eddy_shell_alignment_parameters</path>
      <size>2171</size>
   </file>
   <file>
      <md5sum>7e0db23168be7a3402e42565da1da6a4</md5sum>
      <name>eddy_unwarped_images.eddy_outlier_report</name>
      <path>100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_outlier_report</path>
      <size>8216</size>
   </file>
   <file>
      <md5sum>2fdc71a8257097b99b36e70757d641d3</md5sum>
      <name>eddy_unwarped_images.eddy_outlier_map</name>
      <path>100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_outlier_map</path>
      <size>127363</size>
   </file>
   <file>
      <md5sum>d779a75a17612c44a1c682310b5be888</md5sum>
      <name>eddy_unwarped_images.eddy_movement_rms</name>
      <path>100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_movement_rms</path>
      <size>15838</size>
   </file>
   <file>
      <md5sum>c8b5bd5e3a1e58cfe73e721ebf0a9632</md5sum>
      <name>eddy_unwarped_images.eddy_parameters</name>
      <path>100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_parameters</path>
      <size>141660</size>
   </file>
   <file>
      <md5sum>e18c13056e5af8b5be919ad318f35c3d</md5sum>
      <name>eddy_unwarped_images.eddy_restricted_movement_rms</name>
      <path>100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_restricted_movement_rms</path>
      <size>16085</size>
   </file>
   <file>
      <md5sum>8fdb960e863512050b108faada7a3c96</md5sum>
      <name>eddy_unwarped_images.eddy_outlier_n_stdev_map</name>
      <path>100206/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_outlier_n_stdev_map</path>
      <size>536216</size>
   </file>
   <file>
      <md5sum>f988fb4d12613ae903be1caed06d18b0</md5sum>
      <name>T1w_acpc_dc_restore_1.25.nii.gz</name>
      <path>100206/T1w/T1w_acpc_dc_restore_1.25.nii.gz</path>
      <size>13256170</size>
   </file>
   <file>
      <md5sum>09d38e5ad2c4da76f6a2e048eda0032a</md5sum>
      <name>ReleaseNotes.txt</name>
      <path>100206/release-notes/ReleaseNotes.txt</path>
      <size>786</size>
   </file>
</manifestFile>
```


The image03 data structure that would be submitted is shown below. The Manifest file is now listed under manifest and image_file is left empty. 

| image | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|------------------|------------------|----------------|---------------|-----|---------------------|------------|----------------------|-------------------------------------------|-------------------|-------------------|----------------|-------------------------|-----------------|------------------------------|-------------------------|------------------------|------------|--------------------|----------------------|------------------|--------------------|--------------|---------------|--------------------------|---------------------|---------------|----------------------|---------------|---------------|---------------|---------------|--------------|---------------|--------------|-------------|-------------|-------------|-------------|-------------|-------------------|-------------------|-------------------|-------------------|-------------------|-----------------------|-------------------|------------|----------------|----------------------|-------------|------------|------------------|---------------------------|-----------------|------------------|----------------|------------|-----------------|-----------|-------------------|------------------|-----------|---------------|-------------|-----------------|-------------------|-------|------|------------------------|-----------------------|--------------|----------|----------|-----------------|--------------------|----------|--------|------------------|
| SUBJECTKEY | SRC_SUBJECT_ID | INTERVIEW_DATE | INTERVIEW_AGE | SEX | COMMENTS_MISC | IMAGE_FILE | IMAGE_THUMBNAIL_FILE | MANIFEST | IMAGE_DESCRIPTION | IMAGE_FILE_FORMAT | IMAGE_MODALITY | SCANNER_MANUFACTURER_PD | SCANNER_TYPE_PD | SCANNER_SOFTWARE_VERSIONS_PD | MAGNETIC_FIELD_STRENGTH | MRI_REPETITION_TIME_PD | FLIP_ANGLE | ACQUISITION_MATRIX | MRI_FIELD_OF_VIEW_PD | PATIENT_POSITION | PHOTOMET_INTERPRET | RECEIVE_COIL | TRANSMIT_COIL | TRANSFORMATION_PERFORMED | TRANSFORMATION_TYPE | IMAGE_HISTORY | IMAGE_NUM_DIMENSIONS | IMAGE_EXTENT1 | IMAGE_EXTENT2 | IMAGE_EXTENT3 | IMAGE_EXTENT4 | EXTENT4_TYPE | IMAGE_EXTENT5 | EXTENT5_TYPE | IMAGE_UNIT1 | IMAGE_UNIT2 | IMAGE_UNIT3 | IMAGE_UNIT4 | IMAGE_UNIT5 | IMAGE_RESOLUTION1 | IMAGE_RESOLUTION2 | IMAGE_RESOLUTION3 | IMAGE_RESOLUTION4 | IMAGE_RESOLUTION5 | IMAGE_SLICE_THICKNESS | IMAGE_ORIENTATION | QC_OUTCOME | QC_DESCRIPTION | QC_FAIL_QUEST_REASON | PET_ISOTOPE | PET_TRACER | DECAY_CORRECTION | TIME_DIFF_INJECT_TO_IMAGE | TIME_DIFF_UNITS | FRAME_START_UNIT | FRAME_END_UNIT | DATA_FILE2 | DATA_FILE2_TYPE | SCAN_TYPE | SLICE_ACQUISITION | SOFTWARE_PREPROC | PULSE_SEQ | EXPERIMENT_ID | SCAN_OBJECT | FRAME_END_TIMES | FRAME_START_TIMES | STUDY | WEEK | EXPERIMENT_DESCRIPTION | VISIT | SLICE_TIMING | BVECFILE | BVALFILE | BVEK_BVAL_FILES | DEVICESERIALNUMBER | PROCDATE | VISNUM | MRI_ECHO_TIME_PD |
| NDAR_INV25KAJM0U | NDAR_INV25KAJM0U | 6/4/17 | 109 | M | MB2 fMRI Fieldmap P |  |  | 100206_3T_Diffusion_preproc_manifest.json | ABCD-fMRI-FM-PA | fMRI | MRI | Philips Medical Systems | Achieva dStream | ["5.3.0", "5.3.0.0"] | 3 | 7 | 52 | [92, 0, 0, 89] |  | HFS | MONOCHROME2 | MULTI COIL |  | No |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 |  |  |  |  | 2.4 |  |  |  | NA |  |  |  |  |  |  |  |  |  | Field Map |  |  |  |  | Live |  |  |  |  |  | baseline_year_1_arm_1 |  |  |  |  | anonb2d4 |  |  | 0.07 |



### How to submit data using a manifest:
Manifest files can be submitted with two NDA data structures, image03 and fmriresults01. Instead of indicating a file in the image_file or derived_files columns, list the JSON file in the Manifest data element column. As of now, data submission for structures that use this new type will need to use the nda-tools vtcmd tool, which is distributed with the nda-tools python package. 
##### Note: As of now, nda-tools will only accept manifest files in JSON format. To submit Manifests in XML format, please use our [swagger interface](https://nda.nih.gov/api/validation/docs/swagger-ui.html#!/validation/uploadManifestUsingPUT) for the validation service instead. 

To submit data with nda-tools, specify the location of your Manifest files:

```
vtcmd image03.csv -m path/to/manifest/files -l path/to/associated/files -t <YourTitle> -d <a description of your submission> -c <collection_id> -b
```

If your associated files are stored in S3, you may optionally pass in an S3 bucket instead of a directory.

```
vtcmd image03.csv -m path/to/manifest/files -s3 <S3Bucket> -pre <if/prefix/exists> -t <YourTitle> -d <a description of your submission> -c <collection_id> -b
```

Each file listed in the Manifest file will be treated as an associated file and uploaded as such. Once the submission is complete, each file will be available in S3 to access individually. 

