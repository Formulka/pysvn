import sys
import pysvn
print( 'Info: pre commit test 1' )

if len(sys.argv) == 4 and sys.argv[3] == 'is_revision':
    print( 'Info: Transaction( %s, %s, is_revision=True) ...' % (sys.argv[1], sys.argv[2]) )
    t = pysvn.Transaction( sys.argv[1], sys.argv[2], is_revision=True )
else:
    print( 'Info: Transaction( %s, %s) ...' % (sys.argv[1], sys.argv[2]) )
    t = pysvn.Transaction( sys.argv[1], sys.argv[2] )

print( 'Info: revproplist() ...' )
all_props = t.revproplist()
for name, value in all_props.items():
    print( '%s: %s' % (name, value) )

print(  'Info: changed() ...' )
changes = t.changed()
change_list = list( changes.items() )
change_list.sort()
for name, (action, kind, text_mod, prop_mod) in change_list:
    print( '%s: action=%r, kind=%r, text_mod=%r, prop_mod=%r' % (name, action, kind, text_mod, prop_mod) )
    if action != 'D':
        all_props = t.proplist( name )
        for prop_name, prop_value in all_props.items():
            print( '     %s: %s' % (prop_name, prop_value) )
        if kind == pysvn.node_kind.file:
            print( '     contents: %r' % t.cat( name ) )

print( 'Info: changed( copy_info=True ) ...' )
changes = t.changed( copy_info=True )
change_list = list( changes.items() )
change_list.sort()
for name, (action, kind, text_mod, prop_mod, copyfrom_rev, copyfrom_path) in change_list:
    print( '%s: action=%r, kind=%r, text_mod=%r, prop_mod=%r copyfrom_rev=%r copyfrom_path=%r' %
            (name, action, kind, text_mod, prop_mod, copyfrom_rev, copyfrom_path) )
    if action != 'D':
        all_props = t.proplist( name )
        for prop_name, prop_value in all_props.items():
            print( '     %s: %s' % (prop_name, prop_value) )
        if kind == pysvn.node_kind.file:
            print( '     contents: %r' % t.cat( name ) )

print( 'Info: list() ...' )
def recursive_list( path ):
    entries = t.list( path )
    entry_list = list( entries.items() )
    entry_list.sort()
    for name, kind in entry_list:
        full = '%s/%s' % (path, name)
        print( '%s: kind=%r' % (full, kind) )
        if kind == pysvn.node_kind.dir:
            recursive_list( full )
recursive_list( '' )

sys.exit( 0 )
