%include %{_rpmconfigdir}/macros.python

# Defaults to --with-mysql unless --without mysql is specified, should this change?
%{!?_without_mysql: %{!?_with_mysql: %define _with_mysql --with-mysql}}
# Defaults to --without-psycopg2
%{!?_with_psycopg2: %{!?_without_psycopg2: %define _without_psycopg2 --without-psycopg2}}

Name:		clusto
Version:	0.7.8
Release:	0%{?dist}
Summary:	Tools and libraries for organizing and managing infrastructure

Group:		Applications/System
License:	BSD
URL:		http://github.com/clusto/clusto
Source0:	https://github.com/clusto/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

BuildRequires:	python-devel
BuildRequires:	python-sphinx-doc
%if 0%{?fedora} >= 8
BuildRequires:	python-setuptools-devel
%else
BuildRequires:	python-setuptools
%endif
Requires:	python-sqlalchemy >= 0.5
Requires:	ipython
Requires:	libvirt-python
Requires:   python-IPy
Requires:   scapy >= 2.0
Requires:   PyYAML
%{?_with_mysql:Requires: MySQL-python}
%{?_with_psycopg2:Requires: python-psycopg2}

%description
Clusto is a cluster management tool. It helps you keep track of your inventory,
where it is, how it's connected, and provides an abstracted interface for
interacting with the elements of the infrastructure.


%prep
%setup -q -n %{name}-%{version}


%build
%{__python} -c 'import setuptools; execfile("setup.py")' build
# Build documentation
cd doc
make html
rm -f .build/html/.buildinfo


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
%{__python} -c 'import setuptools; execfile("setup.py")' install -O1 --skip-build --root %{buildroot}
# Create additional directories
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_libexecdir}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}/web
cp conf/* %{buildroot}%{_sysconfdir}/%{name}/
cp contrib/*.py %{buildroot}%{_libexecdir}/%{name}/
cp -R web/static/* %{buildroot}%{_datadir}/%{name}/web/


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README.md LICENSE doc/.build/html
%config(noreplace) %{_sysconfdir}/%{name}
%{py_sitedir}/%{name}*
%attr(0755, root, root) %{_libexecdir}/%{name}/*
%attr(0755, root, root) %{_datadir}/%{name}/*
%attr(0755, root, root) %{_bindir}/*


%changelog
* Wed Jul 29 2015 Mike Newton <mike@delusion.org> - 0.7.8-0
- Merge pull request #71 from motivator/rm_bugs (Mike Newton)
- Merge pull request #72 from motivator/ipython_version (Mike Newton)
- ipython 4.0.0b1 does not work (yet) (Mike Newton)
- better exception handling and remove errant import (Mike Newton)
- better way to test on deallocate. also updated tests. (Mike Newton)
- be less greedy with deallocation (Mike Newton)
- make resource tests more complete (Mike Newton)
- actually use number to keep track of resources and resource attributes (Mike Newton)
- Merge pull request #69 from yiranwang52/master (Jorge Gallegos)
- Fix unclusto() for "json" datatype (Yiran Wang)
- Merge pull request #67 from daradib/tree-command (Jorge Gallegos)
- Dedent docstring for command help (Dara Adib)
- Move clusto-tree to commands (Dara Adib)
- Merge pull request #66 from jamesonjlee/jamesonjlee-patch-1 (Jeremy Grosser)
- catch LookUpError to return None (Jameson)
- Merge pull request #65 from ctrlhxj/add_prefetch (Jeremy Grosser)
- add prefetch to get attributes in one query (Xiaojian Huang)
- Merge pull request #64 from daradib/clusto-attr-tree (Jorge Gallegos)
- Remove extra newline for each object in clusto-tree (Dara Adib)
- Combine clusto-attr-tree and clusto-tree scripts (Dara Adib)
- Change clusto-attr-tree attribute output format (Dara Adib)
- Add clusto-attr-tree script (Dara Adib)
- Merge pull request #62 from mgeggie-uber/master (Jorge Gallegos)
- Adding the --force/-f options to force taking over a console session. Setting default value to False in the add_argument. (Mike Geggie)
- Revert "Adding the --force flag to clusto-console so console sessions can be acquired by force" (Mike Geggie)
- Adding the --force flag to clusto-console so console sessions can be acquired by force (Mike Geggie)
- Merge pull request #60 from AltanAlpay/setattr (Jeremy Grosser)
- Merge pull request #59 from AltanAlpay/addattr (Jeremy Grosser)
- setattr returns '400 Element Not Found' if related object not found (Altan Alpay)
- addattr LookupError translates to '400 Element Not Found' (Altan Alpay)
- addattr to support relational and integer values (Altan Alpay)
- addattr to support relational and integer values (Altan Alpay)
- addattr to support relational and integer values (Altan Alpay)
- Merge pull request #57 from dansawyer73/rename_properties_fix (Jorge Gallegos)
- Merge pull request #58 from Roguelazer/adjacency_map (Jorge Gallegos)
- add a new method which returns the entire clusto adjacency map in one pass (James Brown)
- Add testcase testRenameWithProperties for testing rename and preserving _properties (Dan Sawyer)
- When renaming an object, update attributes that are also properties rather than adding them. This will avoid a duplicate copy of all properties. (Dan Sawyer)
- Merge pull request #56 from sloppyfocus/better_exceptions (Jorge Gallegos)
- Fix get_by_name to not swallow all database errors (Daniel Chen)
- Merge pull request #55 from JeremyGrosser/cidr_attrs (Jeremy Grosser)
- Make _int_to_cidr a classmethod for consistency (Jeremy Grosser)
- Add a key=ip,subkey=cidr attribute to entities which have an allocated IP (Jeremy Grosser)
- Merge pull request #54 from JeremyGrosser/fix_format_string (Jorge Gallegos)
- Fix a format string in clusto-pool error message (Jeremy Grosser)
- Merge pull request #52 from motivator/moti_epool (Jeremy Grosser)
- this will be 0.8 at some point (Jorge Gallegos)
- Merge pull request #38 from thekad/strict_get_from_pools (Jorge Gallegos)
- Merge branch 'master' into strict_get_from_pools (Jorge Gallegos)
- Merge pull request #51 from thekad/fix-deallocate (Jorge Gallegos)
- PEP8 fixes (Jorge Gallegos)
- This should fix the error down below (Jorge Gallegos)
- Merge pull request #49 from sloppyfocus/speedup_merge_container_attributes (Jorge Gallegos)
- Speed up attrs(merge_container_attrs=True) calls (Daniel Chen)
- Merge pull request #39 from thekad/base_types (Jorge Gallegos)
- Merge pull request #48 from sloppyfocus/prune_search_children (Jorge Gallegos)
- Prune children searches (Daniel Chen)
- Merge pull request #47 from sloppyfocus/more_speedups (Jeremy Grosser)
- Add grandchildren contents() test (Daniel Chen)
- Fix linting errors (Daniel Chen)
- Abstract _get_contents into a separate method (Daniel Chen)
- Merge pull request #46 from sloppyfocus/speed_up_stuff (Jeremy Grosser)
- Change ValueError to AssertionError (Daniel Chen)
- Fixed a bug due to bad linting (Daniel Chen)
- Add tests for clusto.util (Daniel Chen)
- Modify contents() to batch up 500 rows at a time (Daniel Chen)
- Remove more trailing whitespace (Daniel Chen)
- Remove trailing whitespace (Daniel Chen)
- Remove content_attrs filter for pool (Daniel Chen)
- Fix bad in_ clause (Daniel Chen)
- Turn off debugging (Daniel Chen)
- Speed up contents lookup (Daniel Chen)
- Filter by pool (Daniel Chen)
- Merge pull request #44 from JeremyGrosser/cleanup_reboot (Jeremy Grosser)
- Merge pull request #45 from JeremyGrosser/command_tracebacks (Jeremy Grosser)
- Log tracebacks with newlines (Jeremy Grosser)
- Log traceback as debug (Jeremy Grosser)
- Dropping travis support for 2.6 (Jorge Gallegos)
- Don't hide full tracebacks for clusto commands, it makes debugging difficult (Jeremy Grosser)
- Cleanup reboot command, add --batch option to disable confirmation prompt, --method option to pass a string to reboot() (Jeremy Grosser)
- Merge pull request #42 from thekad/master (Jorge Gallegos)
- tee hee (Jorge Gallegos)
- Bumping spec and debian/changelog (Jorge Gallegos)
- Resource managers dont't overload type (Jorge Gallegos)
- Add a get_from_entities() (Jorge Gallegos)
- get_from_pools() should *only* get from _pools_ (Jorge Gallegos)
- test for ExclusivePool membership before inserting into another pool (Mike Newton)

* Fri Jan 24 2014 Jorge A Gallegos <kad@blegh.net> - 0.7.7-0
- Bumping version, preparing for release (Jorge Gallegos)
- Merge pull request #41 from motivator/pr/40 (Jeremy Grosser)
- add delete() to Counter; add testPoolDelete() (Mike Newton)
- Add query to Counter (Daniel Chen)
- Delete references from the counters table (Daniel Chen)
- Set memcache warning to debug level (Jeremy Grosser)
- Fix whitespace in debian/changelog (Jeremy Grosser)
- Put the "NUM" column back in clusto-attr show output (Jeremy Grosser)

* Mon Nov 4 2013 Mike Newton <mike@delusion.org> - 0.7.6
- Merge pull request #35 from thekad/master (Jeremy Grosser)
- Adding more options to get_conf (Jorge Gallegos)
- Updated travis notifications (Jorge Gallegos)
- Merge pull request #34 from motivator/delete-noversion (Jorge Gallegos)
- Merge pull request #33 from synack/ipmanagers (Jorge Gallegos)
- delete from database when versioning is off (Mike Newton)
- Add IPManager.get_ip_managers classmethod (Jeremy Grosser)
- Enable versioning during unit tests (Jeremy Grosser)
- Versioning disabled by default (Jeremy Grosser)
- Add -n --number option to clusto-attr (Jeremy Grosser)
- Remove logging fileConfig and explicitly configure audit logging so that we don't break tools that
* Tue Oct 22 2013 Jorge A Gallegos <kad@blegh.net> - 0.7.5-0
- It'd been quite a while since spec file was loved (Jorge Gallegos)
- Merge pull request #32 from thekad/master (Jorge Gallegos)
* Tue Oct 22 2013 Jorge A Gallegos <kad@blegh.net> - 0.7.5-0
- Bumping version slightly (Jorge Gallegos)
- Got rid of a deprecation warning in clusto-shell (Jorge Gallegos)
- Pull the requirements from the main setup.py file (Jorge Gallegos)
- I immediately regret this decision (Jorge Gallegos)
- Merge pull request #30 from Roguelazer/cleaner_client_ids (Jeremy Grosser)
- Merge pull request #31 from Roguelazer/str_basestring (Jeremy Grosser)
- Tagging 0.7.4 (Jeremy Grosser)
- ignore client_ids that don't parse according to this one scheme (James Brown)
- Merge pull request #29 from synack/audit_log (Jeremy Grosser)
- Add audit logging (Jeremy Grosser)
- Make clusto-dhcpd a bit more robust, assume dhcp only runs on RFC1918 subnets (Jeremy Grosser)
- Fix clusto-dhcpd script (Jeremy Grosser)
- Bump version to 0.7.3 (Jeremy Grosser)
- Install clusto-dhcpd (Jeremy Grosser)
- Fix get_type_name failure (Jeremy Grosser)
- Tag 0.7.2 (really this time) (Jeremy Grosser)
- Bump version to 0.7.1 (Jeremy Grosser)
- Tagging new release 0.6.0 (Jeremy Grosser)
- Merge pull request #28 from synack/optional_versions (Jorge Gallegos)
- Set series to precise so that we can push to a PPA (Jeremy Grosser)
- Switch to dh_python2 (Jeremy Grosser)
- Bump version, fix debian docs, add license to setup.py (Jeremy Grosser)
- Make clusto versioning optional. Once disabled, new versions are simply not created. This allows existing databases with historical versions to work compatibly. (Jeremy Grosser)
- use basestring instead of str in a few places in clusto (James Brown)
- Merge pull request #26 from motivator/attr_cmp (motivator)
- do not compare number - kad mentions this might not fit with the rest of number's use (Mike Newton)
- Merge pull request #25 from motivator/attr_cmp (motivator)
- make __eq__ compare more than just key/value (Mike Newton)
- Merge pull request #24 from synack/http_wsgi (Jorge Gallegos)
- Load clusto config on module init with clusto.services.http (Jeremy Grosser)
- Add handy bash aliases to clusto docs (Jeremy Grosser)
- Merge pull request #23 from synack/listpool (Jeremy Grosser)
- Make clusto-list-pool a bit smarter (Jeremy Grosser)
- Playing with deps (Jorge Gallegos)
- Merge pull request #22 from motivator/moti_getbyip (kad)
- add a get_by_ip() method (Mike Newton)
- Don't need add_subparser anymore (Jorge A Gallegos)
- Add clusto-rename command (Jeremy Grosser)
- updating readme to be markdown (Jorge A Gallegos)
- Simplify some things, also eliminate duplicates (Jorge A Gallegos)
- Dropping assert_unicode from schema.py (Jorge A Gallegos)
- Forgot to fix this part (Jorge A Gallegos)
- No need to override this anymore (Jorge A Gallegos)
- Not all objects share the same ipman (Jorge A Gallegos)
- You can now override the formatter class (Jorge A Gallegos)
- Fixing clusto-tree to work with current options (Jorge A Gallegos)
- Merge pull request #20 from thekad/master (kad)
- Set the starting namespace for clusto shell (Jorge A Gallegos)
- Virtual servers should only add 2 extra methods (Jorge A Gallegos)
- Merge pull request #19 from thekad/issues/16 (kad)
- Added a testGetFromPools test (Jorge A Gallegos)
- This should raise errors on non-existent names (Jorge A Gallegos)
- Merge pull request #18 from motivator/moti_sadep2 (kad)
- schemy.py updates (remove import *s, update DDL events for sqlalchemy >= 0.7); sqlalchemy >= 0.7 now required (Mike Newton)
- Merge pull request #17 from motivator/moti_basicdrivers (motivator)
- add BasicFirewall and BasicLoadBalancer drivers (Mike Newton)
- Merge pull request #15 from motivator/moti_location1 (kad)
- add Location.insert() instead of using inherited Driver.insert() (Mike Newton)
- Making some minor improvements to captcha function (Jorge A Gallegos)
- This is just wrong (Jorge Gallegos)
- Merge pull request #14 from motivator/moti_bindip (motivator)
- r0n noticed i forgot to change netmasks in my tests...oops (Mike Newton)
- Merge pull request #13 from motivator/moti_bindip (kad)
- update tests for multiple ip bind_ip_to_osport (Mike Newton)
- fix bind_ip_to_osport so ip binds correctly (Mike Newton)
- Removing 2.5 CI (Jorge A Gallegos)
- Adding clusto to travis-ci (Jorge A Gallegos)
- Remove SQLAlchemy version limit, bump to version 0.5.38 (Jeremy Grosser)
- Allow depending on newer IPython (Jeremy Grosser)
- Revert "Rework config and re-introduce clusto.init_script" (Jeremy Grosser)
- Revert "Set SESSION.memcache=None by default" (Jeremy Grosser)
- Set SESSION.memcache=None by default (Jeremy Grosser)
- Rework config and re-introduce clusto.init_script (Jeremy Grosser)
- Cast "number" to an integer (Jeremy Grosser)
- Merge pull request #12 from egon010/master (Paul Lathrop)
- Merge branch 'master' of github.com:egon010/clusto (James Downs)
- Adding support for IPython >= 0.11 (fixed embedded tabs) (James Downs)
- Adding support for IPython >= 0.11 (James Downs)
- Merge pull request #11 from motivator/listpool (motivator)
- allow list-pool to accept 1-2 pool arguments (Mike Newton)
- Merge pull request #10 from synack/master (Jeremy Grosser)
- Depend on python-pkg-resources (Jeremy Grosser)
- Add clusto initdb (Jeremy Grosser)
- Missing comma in example config... Could've sworn I fixed this before... (Jeremy Grosser)
- Helps if you actually add the files you want... (Jeremy Grosser)
- Update changelog (Jeremy Grosser)
- Add clusto-list-all command (Jeremy Grosser)
- Packaging cleanup, pass lintian (mostly) (Jeremy Grosser)
- Fix maintainer email (Jeremy Grosser)
- arch=all (Jeremy Grosser)
- Merge pull request #9 from plathrop/cage-object (kad)
- Packaging updates: add BasicCage, dependency on python-setuptools. (Paul Lathrop)
- Add a BasicCage driver. (Paul Lathrop)
- Update debian/control (Jeremy Grosser)
- Merge pull request #8 from motivator/fixcopyright (kad)
- fix the debian/copyright license info (Mike Newton)
- Slight mistake on get() (Jorge A Gallegos)
- Split this to https://github.com/clusto/clusto-ec2 (Jorge A Gallegos)
- Somehow this lil' thing got lost (Jorge A Gallegos)
- Writing a setup.py for easy packaging (Jorge A Gallegos)
- Use RawTextHelpFormatter for Paul's pleasure (Jorge Gallegos)
- Merge pull request #6 from synack/minimal (kad)
- Merge pull request #7 from motivator/moti-loadconfig (kad)
- change load_config() to not require config file (Mike Newton)
- Support importing plugins with CLUSTOPLUGINS environment variable or plugins option in clusto.conf (Jeremy Grosser)
- clusto-shell doesn't work with ipython 0.11 yet (Jorge A Gallegos)
- Re-add dhcp/snmp stuff (Jeremy Grosser)
- Re-integrate clusto-httpd (Jeremy Grosser)
- Pull clusto-httpd back in (Jeremy Grosser)
- Fix clustoec2 README (Jeremy Grosser)
- Re-adding EC2 support in the form of the clustoec2 extension (Jeremy Grosser)
- Move digg drivers into a separate package as an example of how to extend clusto (Jeremy Grosser)
- Make tests pass with no extended drivers (Jeremy Grosser)
- Minimal build of clusto with only core implementations (Jeremy Grosser)
- Updating IP ranges for ec2 (Jorge A Gallegos)
- Boto 2.0 has been released (Jorge A Gallegos)
- Merge branch 'upstream' (Jorge A Gallegos)
- Merge pull request #5 from lindenlab/master (kad)
- Fixing sqlalchemy versioning (Jorge A Gallegos)
- Merge branch 'upstream' (Jorge A Gallegos)
- Popular demand: make it easier to write messy code (Jorge A Gallegos)
- A little bit of sugar added to clusto-shell: (Jorge A Gallegos)
- Fixed init_script in commands of the form clusto-* (Jorge A Gallegos)
- A little bit of sugar added to clusto-shell: (Jorge A Gallegos)
- Fixed init_script in commands of the form clusto-* (Jorge A Gallegos)
- Merge branch 'master' of github.com:thekad/clusto (Jorge A Gallegos)
- Fixing sqlalchemy versioning (Jorge A Gallegos)
- Adding support for tagging/naming instances. (Jorge A Gallegos)
- Raise exception when doing a rollback when no transaction was started. (Ron Gorodetzky)
- clear transaction counter when clearing session (Ron Gorodetzky)
- clean up sql for the common case of querying against the current version (Ron Gorodetzky)
- Raise exception when doing a rollback when no transaction was started. (Ron Gorodetzky)
- clear transaction counter when clearing session (Ron Gorodetzky)
- clean up sql for the common case of querying against the current version (Ron Gorodetzky)
- Merged with clusto/clusto master. (Lex Linden)
- Fixing sqlalchemy versioning (Jorge A Gallegos)
- sqlalchemy.exceptions are actually sqlalchemy.exc (Jorge A Gallegos)
- sqlalchemy.exceptions are actually sqlalchemy.exc (Jorge A Gallegos)
- Adding EC2IPManager to the ec2 helper (Jorge A Gallegos)
- Updating list of amazon IPs (Jorge A Gallegos)
- Adding EC2IPManager to the ec2 helper (Jorge A Gallegos)
- Updating list of amazon IPs (Jorge A Gallegos)
- Adding support for tagging/naming instances. (Jorge A Gallegos)
- Turns out is not Zip Safe after all (Jorge A Gallegos)
- s/Manger/Manager/ I got you, Ron. Finally. (Jorge A Gallegos)
- * Adde timestamp functionality to do_attr_query (Michael Kania)
- Darnit.  Missed a case where I could end up storing u'None' instead of None. (Lex Linden)
- Eradicated (hopefully) this warning:   SAWarning: Unicode type received non-unicode bind param value (Lex Linden)
- Don't re-raise exceptions; allow existing exception to propagate up so that the caller can more easily debug. (Lex Linden)
- Driver.__new__ should allow any number of arguments to be passed to a subclass's constructor. (Lex Linden)
- Driver.__new__ should not require a name, driver, or entity parameter to be passed.  Let the subclass decide for itself if it wants to require this. (Lex Linden)
- * Have specific exceptions for noninteger port numbers and port numbers less than 1. (Dynamike Linden)
- Really fixing basicrack.py this time (Joshua Tobin)
- Bug fix in basicrack.py (Joshua Tobin)
- Adding functionality to basicrack.py to allow devices other than Device to be inserted into a rack (Joshua Tobin)
- Merge branch 'upstream' into argparse (Jorge A Gallegos)
- Sorry 'bout that (Jorge A Gallegos)
- Fixing typo in portmixin.py (Joshua Tobin)
- Fuck boilerplate, init_arguments() does all that (Jorge A Gallegos)
- Added missing srcdir variable (Jorge A Gallegos)
- Some cosmetic changes, require sqla >= 0.6.3 (Jorge A Gallegos)
- Ported deallocate (Jorge A Gallegos)
- I wasn't returning the exit code here (Jorge A Gallegos)
- Added iteration support for Drivers. (Lex Linden)
- Small changes, still trying to figure out things (Jorge A Gallegos)
- Debian bump (Jorge A Gallegos)
- Revert simplegeo's changes to static web interface (Jeremy Grosser)
- Remove simplegeo changelog entries (Jeremy Grosser)
- Prepared changelog for build 8 (Simple Geebus)
- Add system.os (Jeremy Grosser)
- Fix http json.loads (Jeremy Grosser)
- Depend on webob for clusto-httpd (Jeremy Grosser)
- Prepared changelog for build 7 (Simple Geebus)
- Install clusto-barker-consumer (Jeremy Grosser)
- Prepared changelog for build 5 (Simple Geebus)
- Set source format (Jeremy Grosser)
- Barker and packaging patches (Jeremy Grosser)
- allow deallocation even if instance already doesn't exist (Ron Gorodetzky)
- change hidden attr escape char to @ (Ron Gorodetzky)
- add an underscore test (Ron Gorodetzky)
- add data to puppet-node2 (Ron Gorodetzky)
- add t1.micro instance type (Ron Gorodetzky)
- update ec2 ip ranges (Ron Gorodetzky)
- fix ec2virtualserver update_metadata to run at least once when wait=False (Ron Gorodetzky)
- add region to userdata template dictionary (Ron Gorodetzky)
- allow ec2virtualserver.update_metadata to wait until state=='running' (Ron Gorodetzky)
- add update_metadata to base Driver (Ron Gorodetzky)
- add ec2 helper to create all ec2 objects (Ron Gorodetzky)
- add basic zone object and EC2Zone driver (Ron Gorodetzky)
- add EC2Region as a datacenter type (Ron Gorodetzky)
- fix locations __init__ files (Ron Gorodetzky)
- let get_or_create take **kwargs (Ron Gorodetzky)
- add clusto-puppet-node2 command (Ron Gorodetzky)
- fix post_*allocation calls (Ron Gorodetzky)
- move EC2IPManager use_ip setup and update_metadata to allocation hooks (Ron Gorodetzky)
- add post_automatic_allocation and post_allocation hooks to ResourceManager (Ron Gorodetzky)
- make get_ip_manager work with any ipmanager type (Ron Gorodetzky)
- fix updating reserved ip list from ec2 and ip allocation (Ron Gorodetzky)
- fix conversion/storage of ip value in ec2ipmanager (Ron Gorodetzky)
- fix ResourceTypeException import (Ron Gorodetzky)
- update ec2ipmanager ip list (Ron Gorodetzky)
- update packaging to depend on boto and mako (Ron Gorodetzky)
- make ec2_user_data a mako template so clusto data (only entity name now) can be replaced (Ron Gorodetzky)
- clear ec2server metadata when deallocating its resources (Ron Gorodetzky)
- add real IP support to ec2virtualserver and initial metadata functions (Ron Gorodetzky)
- if merge_container_attrs is true then attr_value should return the value closest to _this_ thing (Ron Gorodetzky)
- update ipmanager (Ron Gorodetzky)
- add IPMixin to BasicVirtualServer (Ron Gorodetzky)
- initial implementation of EC2IPManager (Ron Gorodetzky)
- cleanup ipmanager ipy to int conversation (Ron Gorodetzky)
- set number when setting additional_attrs in EC2VMManager (Ron Gorodetzky)
- pass aws auth info when connecting to other regions (Ron Gorodetzky)
- remove difference between default:us-east-1 and us-east-1.  Both will use the default connection. (Ron Gorodetzky)
- add separate additional attrs for ec2 resources for quicker lookups (Ron Gorodetzky)
- add security_group support (Ron Gorodetzky)
- check parents when checking ec2_allow_termination (Ron Gorodetzky)
- make default ec2_region "default:us-east-1" (Ron Gorodetzky)
- add console support for EC2VirtualServer (Ron Gorodetzky)
- handle default us-east-1 region and explicit us-east-1 regions separately (Ron Gorodetzky)
- initial EC2 support with very basic documentation (Ron Gorodetzky)
- remove dependency on BasicServer and BasicVirtualServer from VMManager (Ron Gorodetzky)
- add get_resource_manager method to ResourceManager plus whitespace cleanups (Ron Gorodetzky)
- add support for storing jsonable data (Ron Gorodetzky)
- minor doc and whitespace cleanups (Ron Gorodetzky)
- implement get_by_names (Ron Gorodetzky)
- add docstring to get_by_name (Ron Gorodetzky)
- Add missing dependencies to setup.py (Jeremy Grosser)
- Get rid of annoying XenVirtualServer (Jeremy Grosser)
- clusto-http: Remove non-json responses, fix content types, simplify dumps method (Jeremy Grosser)
- Improve error message for clusto-dancer. (Warren Turkal)
- python-sqlite and python-memcache are not strictly required except to run tests, so make them recommends (Lex Linden)
- Only need python-sqlite (>= 0.6.3), not (>= 0.6.4). (Lex Linden)
- Remove python-sqlalchemy from build-depends.  It's not necessary to build clusto (only to test it). (Lex Linden)
- Added some debugging/info lines (Jorge A Gallegos)
- Added iteration support for Drivers. (Lex Linden)
- Coerce values to be unicode objects (Jorge A Gallegos)
- Finished puppet-node, got rid of digg sauce (Jorge A Gallegos)
- Ported clusto-console, got rid of digg stuff (Jorge A Gallegos)
- Small changes, still trying to figure out things (Jorge A Gallegos)
- I think allocate is mostly done (Jorge A Gallegos)
- Adding assert_driver to get_by_name (Jorge A Gallegos)
- Ported clusto-reboot. Happy birthday to me. (Jorge A Gallegos)
- FAI Defaults to No (Jorge A Gallegos)
- clusto-fai (Jorge A Gallegos)
- Removing unnecessary config parsing (Jorge A Gallegos)
- Add support for get_conf default (Jorge A Gallegos)
- Forgot indentation mode (Jorge A Gallegos)
- Adding clusto-attr and making setup.py behave (Jorge A Gallegos)
- Adding support to include other files in config (Jorge A Gallegos)
- Adding json and yaml output options (Jorge A Gallegos)
- You don't need glob (Jorge A Gallegos)
- chmod +x shell.py (Jorge A Gallegos)
- Adding the list-pool command (Jorge A Gallegos)
- Two changes to script_helper to deal with _ and -: (Jorge A Gallegos)
- Adding the clusto-pool command (Jorge A Gallegos)
- Adding *.db to .gitignore (Jorge A Gallegos)
- Forgot I moved these to src/clusto/commands (Jorge A Gallegos)
- We don't need __all__ anymore (Jorge A Gallegos)
- Changes to the clusto frontend:  - Adding doc strings  - Account for commands with underscores to be translated to slashes  - Commands are now read from the FS items, not from __all__, this    so we can split commands in packages later without the need to    update the commands/__init__.py file (Jorge A Gallegos)
- Adding vim swap files to gitignore (Jorge A Gallegos)
- Adding clusto-info script (Jorge A Gallegos)
- Better wording, variables are a bit more explicit (Jorge A Gallegos)
- Two changes, one cosmetic the other functional: (Jorge A Gallegos)
- Some cleanup wrt scripts (Jorge A Gallegos)
- Updated setup.py to Ron's current email address (Jorge A Gallegos)
- Some environment variables (Jorge A Gallegos)
- Just adding a kwarg (Jorge A Gallegos)
- Taking advantage of argparse magic (Jorge A Gallegos)

* Wed Jan 19 2011 Jorge A Gallegos <kad@blegh.net> - 0.5.32-4
- add connection cycling (Ron Gorodetzky)
- Fix stupid mistake in spec dates (Jorge A Gallegos)
- clusto-dancer should be in the contrib dir (Jorge A Gallegos)

* Wed Jan 19 2011 Jorge A Gallegos <kad@blegh.net> - 0.5.32-3
- aptitude is stupid (Jorge A Gallegos)

* Tue Oct 19 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.32-2
- The DHCP server now queries the DB directly instead of going thru
  the API
- Fixing the whole suggests/recommends thing
- We need sqlalchemy 0.6.4

* Mon Oct 18 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.32-1
- 755 (Jorge Gallegos)
- Adding ability to pass a default argument to the config getter
  (Jorge Gallegos)
- keep del_attrs from removing hidden attrs by default (Ron
  Gorodetzky)
- initial feature complete version (William Francis)
- new clusto-mysql script (William Francis)

* Thu Sep 30 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.31-6
- Adding the web interface to the package (Jorge A Gallegos)

* Mon Sep 27 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.31-5
- JS runs on the client... (Jorge A Gallegos)

* Mon Sep 27 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.31-4
- I broke get_entities. I fixed get_entities. (Jorge A Gallegos)

* Wed Sep 22 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.31-3
- Some unicode fixes (Jorge A Gallegos)

* Mon Sep 20 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.31-2
- Fixing a stupid bug (Jorge A Gallegos)
- Adding clusto-orphans script (Jorge A Gallegos)

* Thu Sep 16 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.31-1
- Initial memcache support

* Mon Jul 12 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.29-2
- Fixed %files section

* Mon Jun 28 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.29-1
- add tests for reserving resources
- Adding 'deallocate' command
- Patched list-pool so it doesn't barf when the content is a pool (or
  any other object with no get_ips() method)

* Sat May 8 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.27-3
- Use standard python macros

* Thu May 6 2010 Jeremy Grosser <synack@digg.com> - 0.5.27-2
- Fixed make_tarball.sh script

* Wed May 5 2010 Jeremy Grosser <synack@digg.com> - 0.5.27-1
- Version bump

* Wed May 5 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.26-4
- Adding python-IPy dependency

* Wed May 5 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.26-3
- Packager should go in ~/.rpmmacros

* Tue May 4 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.26-2
- Moved contrib from /var/lib/clusto to /usr/libexec/clusto
- Added sysconf directory defaults
- Added scapy dependency
- Added libvirt-python dependency
- Added mysql conditional dependency (defaults to --with)
- Added psycopg2 conditional dependency (defaults to --without)

* Tue May 4 2010 Jorge A Gallegos <kad@blegh.net> - 0.5.26-1
- First spec draft

