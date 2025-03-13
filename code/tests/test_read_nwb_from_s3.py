import unittest
from unittest.mock import patch, MagicMock
import pynwb
import hdmf_zarr
from analysis_wrapper.utils import read_nwb_from_s3  # Replace with the correct import path

class TestReadNWBFromS3(unittest.TestCase):

    @patch('s3fs.S3FileSystem.exists')  # Mock the exists method of S3FileSystem
    @patch('s3fs.S3FileSystem.isdir')  # Mock the isdir method of S3FileSystem
    @patch('s3fs.S3FileSystem.open')  # Mock the open method of S3FileSystem
    @patch('hdmf_zarr.nwb.NWBZarrIO')  # Mock the instantiation of NWBZarrIO
    @patch('pynwb.NWBHDF5IO')  # Mock NWBHDF5IO in the module where it's used
    def test_read_nwb_from_s3_file(self, mock_nwb_hdf5io, mock_nwb_zarrio, mock_open, mock_isdir, mock_exists):
        # Set up the mocks for the file case (using NWBHDF5IO)
        mock_exists.return_value = True
        mock_isdir.return_value = False
        
        # Mock the file-like object that would be returned by S3FileSystem.open()
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Mock the NWBHDF5IO read operation
        mock_hdf5_io = MagicMock()
        mock_nwb_hdf5io.return_value = mock_hdf5_io
        mock_hdf5_io.read.return_value = MagicMock(spec=pynwb.NWBFile)

        # Call the function with a file location
        s3_location = "s3://my-bucket/my-nwb-file.nwb"
        nwb_file = read_nwb_from_s3(s3_location)

        # Assert that the returned object is an instance of NWBFile
        self.assertIsInstance(nwb_file, pynwb.NWBFile)

        # Verify interactions with the mocks
        mock_exists.assert_called_once_with(s3_location)
        mock_isdir.assert_called_once_with(s3_location)
        mock_nwb_hdf5io.assert_called_once_with(mock_file, mode='r')
        mock_hdf5_io.read.assert_called_once()

    @patch('s3fs.S3FileSystem.exists')  # Mock the exists method of S3FileSystem
    @patch('s3fs.S3FileSystem.isdir')  # Mock the isdir method of S3FileSystem
    @patch('s3fs.S3FileSystem.open')  # Mock the open method of S3FileSystem
    @patch('hdmf_zarr.nwb.NWBZarrIO')  # Mock the instantiation of NWBZarrIO
    @patch('pynwb.NWBHDF5IO')  # Mock NWBHDF5IO in the module where it's used
    def test_read_nwb_from_s3_directory(self, mock_nwb_hdf5io, mock_nwb_zarrio, mock_open, mock_isdir, mock_exists):
        # Set up the mocks for the directory case (using NWBZarrIO)
        mock_exists.return_value = True
        mock_isdir.return_value = True
        
        # Mock the Zarr I/O object for NWBZarrIO
        mock_zarr_io = MagicMock()
        mock_nwb_zarrio.return_value = mock_zarr_io
        mock_zarr_io.read.return_value = MagicMock(spec=pynwb.NWBFile)

        # Call the function with a directory location
        s3_location = "s3://my-bucket/my-nwb-directory"
        nwb_file = read_nwb_from_s3(s3_location)

        # Assert the returned object is an instance of NWBFile
        self.assertIsInstance(nwb_file, pynwb.NWBFile)
        
        # Verify interactions with the mocks
        mock_exists.assert_called_once_with(s3_location)
        mock_isdir.assert_called_once_with(s3_location)
        mock_nwb_zarrio.assert_called_once_with(s3_location, mode='r')
        mock_zarr_io.read.assert_called_once()

    @patch('s3fs.S3FileSystem.exists')  # Mock the exists method of S3FileSystem
    def test_file_not_found(self, mock_exists):
        # Simulate file not found (exists returns False)
        mock_exists.return_value = False
        
        # Test with an invalid file path (which should raise an error)
        s3_location = "s3://my-bucket/invalid-nwb-file.nwb"
        
        with self.assertRaises(FileNotFoundError):
            read_nwb_from_s3(s3_location)

if __name__ == '__main__':
    unittest.main()





