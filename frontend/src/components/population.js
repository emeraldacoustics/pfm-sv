import React, { useState } from 'react';
import { Button, notification } from 'antd';
import AWS from 'aws-sdk';
import axios from 'axios';

AWS.config.update({
  accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID, // Use environment variables
  secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY, // Use environment variables
  region: process.env.REACT_APP_AWS_REGION // Use environment variables
});

const s3 = new AWS.S3();

const generateUniqueFilename = (originalFilename) => {
  const timestamp = new Date().toISOString();
  const fileExtension = originalFilename.split('.').pop();
  return `${timestamp}-${Math.random().toString(36).substr(2, 9)}.${fileExtension}`;
};

const convertToCSV = (data) => {
  if (!data.length) return '';
  
  const headers = Object.keys(data[0]);
  const rows = data.map(row =>
    headers.map(header => row[header]).join(',')
  );

  return [...rows].join('\n');
};

const downloadCSV = (data, filename = 'download.csv') => {
  const csv = convertToCSV(data);
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const Population = () => {
  const [lookup, setLookup] = useState(null);
  const [lookupLoading, setLookupLoading] = useState(false);
  const [update, setUpdate] = useState(null);
  const [updateLoading, setUpdateLoading] = useState(false);
  const [initLoading, setInitLoading] = useState(false);

  const handleLookup = async () => {
    if (!lookup) return;
    setLookupLoading(true);
    const filename = generateUniqueFilename(lookup.name);
    const params = {
      Bucket: process.env.REACT_APP_AWS_S3_BUCKET_NAME,
      Key: filename,
      Body: lookup,
      ContentType: lookup.type,
    };

    await s3.upload(params).promise();
    const data = await axios.post(`https://egycsmq8p4.execute-api.us-east-1.amazonaws.com/dev/lookup/populations?url=https://pfm-sv.s3.amazonaws.com/${filename}`)
    downloadCSV(data.data);
    setLookupLoading(false);
    notification['success']({
      description: 'Successfully downloaded the data.'
    });
  }

  const handleUpdate = async () => {
    if (!update) return;
    setUpdateLoading(true);
    const filename = generateUniqueFilename(update.name);
    const params = {
      Bucket: process.env.REACT_APP_AWS_S3_BUCKET_NAME,
      Key: filename,
      Body: update,
      ContentType: update.type,
    };

    await s3.upload(params).promise();
    axios.post(`https://egycsmq8p4.execute-api.us-east-1.amazonaws.com/dev/update/populations?url=https://pfm-sv.s3.amazonaws.com/${filename}`)
      .then(data => {
        notification['success']({
          description: 'Successfully updated the data.'
        });
        setUpdateLoading(false);
      })
      .catch(err=> {
        notification['error']({
          description: err.response.data
        })
        setUpdateLoading(false);
      })
    
  }

  const handleInit = async () => {
    setInitLoading(true)
    await axios.post(`https://egycsmq8p4.execute-api.us-east-1.amazonaws.com/dev/initialize/populations`)
    setInitLoading(false)
    notification['success']({
      description: 'Successfully initialized the data.'
    });
  }

  return (
    <div className="bg-white p-20 shadow-lg rounded-lg">
      <h1 className="text-4xl font-bold mb-5">Population check</h1>
      <div className='flex justify-center'>
      <Button type='primary' onClick={handleInit} loading={initLoading} className='mb-5'>Initialize Data</Button>
      </div>
      <h2 className='text-2xl'>Download - Results</h2>
      <div className='mt-2'>
        <div>
          <label className="text-sm font-medium">CSV file to upload: </label>
          <input
            className="text-sm border border-gray-300 cursor-pointer bg-gray-50 focus:outline-none"
            type="file"
            onChange={e => {
              setLookup(e.target.files[0]);
            }}
          />
        </div>
        <div className='w-full flex justify-center mt-4'>
          <Button type='primary' onClick={handleLookup} loading={lookupLoading}>Download</Button>
        </div>
      </div>
      <h2 className='text-2xl mt-5'>Upload - Data Results</h2>
      <div className='mt-2'>
        <div>
          <label className="text-sm font-medium">CSV file to upload: </label>
          <input
            className="text-sm border border-gray-300 cursor-pointer bg-gray-50 focus:outline-none"
            type="file"
            onChange={e => {
              setUpdate(e.target.files[0]);
            }}
          />
        </div>
        <div className='w-full flex justify-center mt-4'>
          <Button danger type='primary' onClick={handleUpdate} loading={updateLoading}>&nbsp;&nbsp;Upload&nbsp;&nbsp;</Button>
        </div>
      </div>
    </div>
  )
}

export default Population;