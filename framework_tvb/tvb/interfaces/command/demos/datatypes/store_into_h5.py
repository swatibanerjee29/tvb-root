# -*- coding: utf-8 -*-
#
#
# TheVirtualBrain-Framework Package. This package holds all Data Management, and
# Web-UI helpful to run brain-simulations. To use it, you also need do download
# TheVirtualBrain-Scientific Package (for simulators). See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2020, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#

"""
Demo script on how to use tvb-framework default read/write capabilities

.. moduleauthor:: Lia Domide <lia.domide@codemart.ro>
"""

from tvb.core.neocom import h5
from tvb.basic.profile import TvbProfile
from tvb.datatypes.connectivity import Connectivity
from tvb.adapters.datatypes.h5.connectivity_h5 import ConnectivityH5

if __name__ == '__main__':
    TvbProfile.set_profile(TvbProfile.COMMAND_PROFILE)

    # Read from a ZIP
    conn_ht = Connectivity.from_file()
    conn_ht.configure()

    # Store in a given folder the HasTraits entity
    PATH = "."
    h5.store_complete(conn_ht, PATH)

    # Reproduce the just written file name containing GUID
    file_name = h5.path_for(PATH, ConnectivityH5, conn_ht.gid)

    # Load back from a file name a HasTraits instance
    conn_back = h5.load(file_name)

    # Check that the loaded and written entities are correct
    assert conn_ht.number_of_regions == 76
    assert conn_ht.number_of_regions == conn_back.number_of_regions
