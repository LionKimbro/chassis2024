# Copyright 2024 Lion Kimbro
# SPDX-License-Identifier: BSD-3-Clause
#
# Copyright 2024 Lion Kimbro Redistribution and use in source and
# binary forms, with or without modification, are permitted provided
# that the following conditions are met: 1. Redistributions of source
# code must retain the above copyright notice, this list of conditions
# and the following disclaimer.  2. Redistributions in binary form
# must reproduce the above copyright notice, this list of conditions
# and the following disclaimer in the documentation and/or other
# materials provided with the distribution.  3. Neither the name of
# the copyright holder nor the names of its contributors may be used
# to endorse or promote products derived from this software without
# specific prior written permission.  THIS SOFTWARE IS PROVIDED BY THE
# COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.


from .words import *
from .exceptions import *
from . import chassis


execution_spec = {}  # will be reset in run(...) call


def run(execution_spec = {}):
    """Execute the program, providing a specific execution specification."""
    chassis.run(execution_spec)

def interface(interface_name, required=False):
    """Access the object registered for a given interface.
    
    If it doesn't exist, and it's not required, return None.
    
    If it doesn't exist, and it's required, raises InterfaceUndefined.
    """
    found = chassis.interfaces.get(interface_name)
    if required and not found:
        raise InterfaceUndefined(interface_name)
    return found


