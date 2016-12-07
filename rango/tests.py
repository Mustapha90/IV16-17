from django.test import TestCase
from rango.models import Bares, Tapas
from django.core.urlresolvers import reverse

# Create your tests here.

def add_bar(name, views, likes):
    b = Bares.objects.get_or_create(name=name)[0]
    b.views = views
    b.likes = likes
    b.save()
    return b


class TestsBares(TestCase):
    def test_Visitas(self):
        """
                Asegurar que el numero de visitas es siempre positivo
        """
        bar = Bares(name='test',views=-1, likes=0)
        bar.save()
        self.assertEqual((bar.views >= 0), True)

    def test_slug(self):
        """
                Comprobar la creacion de un campo slug
        """

        bar = Bares(name='bar de pepe',views=0, likes=0)
        bar.save()
        self.assertEqual(bar.slug, 'bar-de-pepe')

class TestViews(TestCase):

    def test_views_sin_bares(self):
        """
        Si no hay categorias, mostrar mensaje
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay categorias.")
        self.assertQuerysetEqual(response.context['categories'], [])
     
    def test_view_con_bares(self):
        """
            Comprobr que los bares se muestran correctamente
        """
        add_bar('test',1,1)
        add_bar('temp',1,1)
        add_bar('tmp',1,1)
        add_bar('tmp test temp',1,1)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")
        num_cats =len(response.context['categories'])
        self.assertEqual(num_cats , 4)

class TestTapas(TestCase):
	def test_crear_tapa(self):
		b = Bares(name='test',views=-0, likes=0)
		b.save()
		t = Tapas(title="tapa", likes=10, category=b)
		t.save()
		self.assertEqual(t.title,"tapa")
