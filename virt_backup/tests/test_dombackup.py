
import datetime
import pytest

from virt_backup.virt_backup import DomBackup
from helper.datetime import MockDatetime


def test_get_disks(fixture_build_mock_domain):
    dombkup = DomBackup(dom=fixture_build_mock_domain)
    expected_disks = {
        "vda": {
            "src": "/var/lib/libvirt/images/test-disk-1.qcow2",
            "type": "qcow2",
        },
        "vdb": {
            "src": "/var/lib/libvirt/images/test-disk-2.qcow2",
            "type": "qcow2",
        }
    }

    assert dombkup._get_disks() == expected_disks


def test_get_disks_with_filter(fixture_build_mock_domain):
    dombkup = DomBackup(dom=fixture_build_mock_domain)
    expected_disks = {
        "vda": {
            "src": "/var/lib/libvirt/images/test-disk-1.qcow2",
            "type": "qcow2",
        },
    }

    assert dombkup._get_disks("vda") == expected_disks


def test_add_disks(fixture_build_mock_domain):
    """
    Create a DomBackup with only one disk (vda) and test to add vdb
    """
    disks = {
        "vda": {
            "src": "/var/lib/libvirt/images/test-disk-1.qcow2",
            "type": "qcow2",
        },
    }
    dombkup = DomBackup(dom=fixture_build_mock_domain, _disks=disks)
    expected_disks = {
        "vda": {
            "src": "/var/lib/libvirt/images/test-disk-1.qcow2",
            "type": "qcow2",
        },
    }
    assert dombkup.disks == expected_disks

    dombkup.add_disks("vdb")
    expected_disks = {
        "vda": {
            "src": "/var/lib/libvirt/images/test-disk-1.qcow2",
            "type": "qcow2",
        },
        "vdb": {
            "src": "/var/lib/libvirt/images/test-disk-2.qcow2",
            "type": "qcow2",
        }
    }
    assert dombkup.disks == expected_disks


def test_add_not_existing_disk(fixture_build_mock_domain):
    """
    Create a DomBackup and test to add vdc
    """
    dombkup = DomBackup(dom=fixture_build_mock_domain)
    with pytest.raises(KeyError):
        dombkup.add_disks("vdc")


def test_get_snapshot_xml(fixture_build_mock_domain):
    dombkup = DomBackup(dom=fixture_build_mock_domain)
    expected_xml = (
        "<domainsnapshot>\n"
        "  <description>Pre-backup external snapshot</description>\n"
        "  <disks>\n"
        "    <disk name=\"vda\" snapshot=\"external\"/>\n"
        "    <disk name=\"vdb\" snapshot=\"external\"/>\n"
        "  </disks>\n"
        "</domainsnapshot>\n"
    )
    assert dombkup.gen_snapshot_xml() == expected_xml


def test_main_backup_name_format(fixture_build_mock_domain):
    dombkup = DomBackup(dom=fixture_build_mock_domain)
    snapdate = datetime.datetime(2016, 8, 15, 17, 10, 13, 0)

    expected_name = "20160815-171013_1_test"
    assert dombkup._main_backup_name_format(snapdate) == expected_name


def test_disk_backup_name_format(fixture_build_mock_domain):
    dombkup = DomBackup(dom=fixture_build_mock_domain)
    snapdate = datetime.datetime(2016, 8, 15, 17, 10, 13, 0)

    expected_name = "20160815-171013_1_test_vda"
    assert dombkup._disk_backup_name_format(snapdate, "vda") == expected_name