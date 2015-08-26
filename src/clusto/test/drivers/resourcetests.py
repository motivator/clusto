from clusto.test import testbase 

from clusto.drivers import *



class ResourceManagerTests(testbase.ClustoTestBase):

    def testAllocate(self):

        rm = ResourceManager('test')
        d = Driver('d')

        rm.allocate(d, 'foo')

        self.assertEqual(rm.owners('foo'), [d])

    def testResourceCount(self):

        rm = ResourceManager('test')
        d = Driver('d')
        
        rm.allocate(d, 'foo')
        rm.allocate(d, 'bar')
        
        self.assertEqual(rm.count, 2)

    def testDeallocate(self):

        rm = ResourceManager('test')
        d = Driver('d')

        rm.allocate(d, 'foo')
        rm.allocate(d, 'bar')
        self.assertEqual(rm.count, 2)

        rm.deallocate(d, 'foo')
        self.assertEqual(rm.count, 1)
        self.assertEqual(rm.owners('foo'), [])

        rm.deallocate(d, 'bar')
        self.assertEqual(rm.count, 0)
        self.assertEqual(rm.owners('bar'), [])

    def testGeneralDeallocate(self):

        rm1 = ResourceManager('test1')
        rm2 = ResourceManager('test2')
        d = Driver('d')

        rm1.allocate(d, 'foo1')
        rm1.allocate(d, 'bar1')

        rm2.allocate(d, 'foo2')
        rm2.allocate(d, 'bar2')
        
        self.assertEqual(rm1.count, 2)
        self.assertEqual(rm2.count, 2)
        self.assertEqual(sorted([x.value for x in rm1.resources(d)]),
                         sorted(['foo1', 'bar1', 'foo2', 'bar2']))

        rm1.deallocate(d)
        self.assertEqual(rm1.count, 0)
        self.assertEqual(rm2.count, 2)

        rm2.deallocate(d)
        self.assertEqual(rm2.count, 0)

        self.assertEqual(sorted(ResourceManager.resources(d)),
                         sorted([]))


    def testResourceAttrs(self):

        
        rm = ResourceManager('test')
        d = Driver('d')

        rm.allocate(d, 'foo')
        rm.allocate(d, 'bar')

        rm.add_resource_attr(d, 'foo', 'attr1', 10)

        self.assertEqual(rm.get_resource_attr_values(d, 'foo', 'attr1'), [10])

        rm.add_resource_attr(d, 'foo', 'attr1', 20)

        self.assertEqual(sorted(rm.get_resource_attr_values(d, 'foo', 'attr1')),
                         sorted([10, 20]))

        rm.del_resource_attr(d, 'foo', 'attr1')
        self.assertEqual(rm.get_resource_attr_values(d, 'foo', 'attr1'), [])

        rm.set_resource_attr(d,'bar', 'attr2', 1)        
        self.assertEqual(rm.get_resource_attr_values(d, 'bar', 'attr2'), [1])

        rm.set_resource_attr(d,'bar', 'attr2', 2)
        self.assertEqual(rm.get_resource_attr_values(d, 'bar', 'attr2'), [2])

    def testReserveResource(self):

        rm = ResourceManager('test')
        d = Driver('d')

        rm.allocate(d, 'foo')

        rm.allocate(rm, 'bar')
        

        self.assertRaises(ResourceException, rm.allocate, d, 'bar')
        
